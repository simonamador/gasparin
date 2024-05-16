import ultralytics
import torch


class ICSI_detect:
  def __init__(self,
               path_detect = 'video_processing/yolomodels/det_model.pt',
               path_segment = 'video_processing/yolomodels/seg_model.pt'):
     
    self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    self.model_det = ultralytics.YOLO(path_detect)
    self.model_seg = ultralytics.YOLO(path_segment)

    self.color_scheme = {'red': (255, 0, 52),
                        'orange': (255, 179, 0),
                        'blue': (0, 71, 189),
                        'light_blue': (7, 185, 252),
                        'green': (154,240, 0),
                        'white': (255, 255, 255),
                        'black': (0, 0, 0)}

    self.label2color = {'oocyte': 'green',
              'holding-pipette-tip': 'blue',
              'needle_tip': 'red',
              'meniscus': 'orange',
              'swimming_sperm': 'green',
              'sperm_box': 'white',
              'sperm_in_needle': 'light_blue'}

  def find_key(self, dict, segment):
      return [key for key,value in dict.items() if value == segment][0]

  # Function to find center-tail and center-head coordinates from segmentation
  # Inputs: Results object from segmentation by YOLO
  # Output: (x,y) coordinates from head and tail, in (head, tail) format
  #   if either head, or tail not found, return None instead of tuple

  def coordinates(self,  results):
    import numpy as np

    ids = results[0].boxes.cls.cpu().numpy()
    conf = results[0].boxes.conf.cpu().numpy()

    key_head = self.find_key(results[0].names, 'head')
    key_tail = self.find_key(results[0].names, 'tail')

    n_head = 0
    n_tail = 0

    if len(ids) > 0:
      if  np.any(ids==key_head):
        id_h = conf == max(conf[ids==key_head])
        mask_head = results[0].masks.xy[id_h.nonzero()[0][0]]
        n_head = mask_head.shape[0]
      if np.any(ids==key_tail):
        id_t = conf == max(conf[ids==key_tail])
        mask_tail = results[0].masks.xy[id_t.nonzero()[0][0]]
        n_tail = mask_tail.shape[0]

        if n_tail == 0:
          c_head = (mask_head[int(n_head/2)]+mask_head[0])/2
          c_head = c_head.astype(int).tolist()
          return c_head, None
        else:
          vert = sum((mask_tail[0]-mask_tail[int(n_tail/2)])**2)
          horz = sum((mask_tail[int(n_tail/4)]-mask_tail[int(n_tail*3/4)])**2)

          if vert < horz:
            c_tail = (mask_tail[int(n_tail/2)]+mask_tail[0])/2
          else:
            c_tail = (mask_tail[int(n_tail/4)]+mask_tail[int(n_tail*3/4)])/2

          if n_head == 0:
            return None, c_tail.astype(int).tolist()
          else:
            c_head = (mask_head[int(n_head/2)]+mask_head[0])/2
            return c_head.astype(int).tolist(), c_tail.astype(int).tolist()
      else:
        return None, None
    else:
      return None, None

  # Function to generate image after center points identification in center
  # of tail and head of preferred sperm
  # Inputs: center head coordinates, center tail coordinates, coordinates of
  #   the lower right sperm box corner, sperm box image, original img.
  # Output: Image with rings surroding the center of head and tail of preferred
  #   sperm, and the sperm box superposed in the top right corner of image.

  def plot_sperm_detect(self, c_head, c_tail, sperm_coord, sperm_box, img):
    import numpy as np
    # # Generate circumference given a specific point
    # def PointsInCircum(r, x, y):
    #   import math
    #   return [[math.cos(2*math.pi/r*j)*r+x,
    #             math.sin(2*math.pi/r*j)*r+y] for j in range(0,100+1)]

    # # Insert cirfumferences in image
    # def center(img, r, x, y, color, color_scheme):
    #   for i in range(0, 10, 1):
    #     positions = [[int(a) for a in b] for b in PointsInCircum(r+i, x, y)]
    #     for (nx,ny) in positions:
    #       img[nx, ny, 0] = color_scheme[color][0]
    #       img[nx, ny, 1] = color_scheme[color][1]
    #       img[nx, ny, 2] = color_scheme[color][2]
    #   return img

    # Insert cirfumferences in image
    def pil_center(img, r, x, y, color, color_scheme):
      from PIL import Image, ImageDraw
      pil_img = Image.fromarray(img)
      draw = ImageDraw.Draw(pil_img)

      xy = [y-r, x-r, y+r, x+r]
      draw.ellipse(xy, outline = color_scheme[color], width = 5)

      img = np.array(pil_img).astype('uint8')
      return img

    # Plot center tail and head rings
    if c_head is not None:
      img = pil_center(img, 30, c_head[1], c_head[0], 'light_blue',
                   self.color_scheme)
    if c_tail is not None:
      img = pil_center(img, 30, c_tail[1], c_tail[0], 'red',
                   self.color_scheme)
      img = pil_center(img, 5, c_tail[1], c_tail[0], 'red',
                   self.color_scheme)

    # Add sperm box in top left corner

    # Add margin
    margin_sz = 20
    img[:sperm_coord[1]+2*margin_sz, :sperm_coord[0]+2*margin_sz, :] = 0
    img[margin_sz//2:sperm_coord[1]+2*margin_sz-margin_sz//2,
        margin_sz//2:sperm_coord[0]+2*margin_sz-margin_sz//2, :] = 255
    # Add sperm box
    sperm_box = np.round((sperm_box - np.min(sperm_box)) / (np.max(sperm_box) - np.min(sperm_box)) * 255)
    img[margin_sz:sperm_coord[1]+margin_sz,
        margin_sz:sperm_coord[0]+margin_sz, :] = sperm_box

    return img

  # Function to plot annotated images, as a substitute of YOLO's plot()
  #   method on a Results object
  # Inputs:
  # Outputs:

  def plot(self, results):
    import numpy as np
    from PIL import Image, ImageDraw
    img = Image.fromarray(results[0].orig_img.copy())
    names = results[0].names
    values = results[0].boxes.cls.tolist()
    labels = [names[int(val)] for val in values]
    boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)

    draw = ImageDraw.Draw(img)
    color = [self.label2color[x] for x in labels]
    legend = dict(zip(set(labels),set(color)))


    for i, box in enumerate(boxes):
      color = legend[labels[i]]
      # for r in range(0,10,1):
      x1, y1, x2, y2 = box
      draw.rectangle([(x1,y1),(x2,y2)], outline = self.color_scheme[color], width = 5)

    return np.array(img), legend

  # Function to resize detected sperm box to a 420x380 size, for segmentation
  #   model, by adding zero-padding or cutting image.
  # Inputs: Sperm box image, new width, new height
  # Output: Resized sperm box image

  def resizing(self, input, w = 420, h = 380):
    import operator
    import numpy as np
    target = (h, w)
    n_img = np.zeros((h, w, 3))
    for i in range(3):
      img = input[:,:,i]
      if (img.shape > np.array(target)).any():
          target_shape2 = np.min([target, img.shape],axis=0)
          start = tuple(map(lambda a, da: a//2-da//2, img.shape, target_shape2))
          end = tuple(map(operator.add, start, target_shape2))
          slices = tuple(map(slice, start, end))
          img = img[tuple(slices)]
      offset = tuple(map(lambda a, da: a//2-da//2, target, img.shape))
      slices = [slice(offset[dim], offset[dim] + img.shape[dim]) for dim in range(img.ndim)]
      result = np.zeros(target)
      result[tuple(slices)] = img
      n_img[:,:,i] = result
    return n_img.astype(np.uint8), slices

  def sperm_selector(self, image):
    import numpy as np

    # Sperm detect
    results = self.model_det.predict(image, conf=.5)
    img = results[0].orig_img
    data = np.array(results[0].boxes.data.tolist())
    x, legend = self.plot(results)

    if len(data)>0:

      # Extract sperm box
      sperm_boxes = data[data[:,5] == 4]
      box = sperm_boxes[sperm_boxes[:,4] == max(sperm_boxes[:,4])].astype(int)[0].tolist()
      x = range(box[0],box[2])
      y = range(box[1],box[3])
      n_img = img.copy()[y, :, :][:, x, :]

      # Resize sperm box
      seg_box, sl = self.resizing(n_img, 420, 380)

      # Sperm box coordinates
      offset_y, offset_x = sl[0].stop, sl[1].start

      # Segment sperm
      results2 = self.model_seg.predict(seg_box)

      # Find center coordinates
      c_h, c_t = self.coordinates(results2)

      if c_t is not None:
        off_tail = [box[0]+c_t[0]-offset_x, box[3]+c_t[1]-offset_y]
        if c_h is not None:
          off_head = [box[0]+c_h[0]-offset_x, box[3]+c_h[1]-offset_y]
        else:
          off_head = None
      else:
        off_tail, off_head = None, None

      # Generate detection image
      detect_img = self.plot_sperm_detect(off_head, off_tail,
      [box[2]-box[0], box[3]-box[1]], n_img, img.copy())

      return detect_img, legend

    else:
      return img, legend

  def ICSI_annotation(self, image):
    import numpy as np

    # Sperm detect
    results = self.model_det.predict(image, conf=.5)
    img, legend = self.plot(results)
    return img, legend