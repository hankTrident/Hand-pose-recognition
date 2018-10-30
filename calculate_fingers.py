import cv2 as cv
import numpy as np
from calculate_contours import get_contours, draw_contours
from calculate_convex_hull import get_convex_hulls, draw_hulls_and_vertices,calculate_convexity_defects
from numpy import linalg

def get_fingers(mask,original_frame):
  frame_copy = np.copy(original_frame)
  contours = get_contours(mask)
  draw_contours(frame_copy,contours)
  
  hulls, clustered_hulls_vertices = get_convex_hulls(contours, mask)
  draw_hulls_and_vertices(frame_copy,hulls,clustered_hulls_vertices,contours)
  
  contours_with_defects = calculate_convexity_defects(contours,clustered_hulls_vertices, cluster_range=10)
  draw_defects(frame_copy,contours_with_defects)

  return frame_copy

def draw_defects(frame_copy, contours_with_defects):
  count_fingers = 0
  for contour_with_defects in contours_with_defects:
    for i in range(0,len(contour_with_defects)):
      triple1 = contour_with_defects[i]
      triple2 = contour_with_defects[i-1]
      new_triple = [triple2[1], triple1[0], triple1[1]]
      if filter_vertices_by_angle(new_triple, 45):
        cv.circle(frame_copy,tuple(new_triple[1]),10,[0,0,255],3)
        count_fingers+= count_fingers


def filter_vertices_by_angle(triple,max_angle):
  a = linalg.norm(triple[0]-triple[2])
  b = linalg.norm(triple[1]-triple[2])
  c = linalg.norm(triple[1]-triple[0])
  angle = np.arccos(((b**2 + c**2 - a**2) /(2 * b * c))) * (180 / np.pi)
  if angle < max_angle:
    return True
  return False
