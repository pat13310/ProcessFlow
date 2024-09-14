import math
from PySide6.QtCore import QPointF


def calculate_rectangle_border(rect, rect_pos, target_point):
    rect = rect.translated(rect_pos)
    lines = [
        (QPointF(rect.left(), rect.top()), QPointF(rect.right(), rect.top())),  # Haut
        (QPointF(rect.right(), rect.top()), QPointF(rect.right(), rect.bottom())),  # Droit
        (QPointF(rect.right(), rect.bottom()), QPointF(rect.left(), rect.bottom())),  # Bas
        (QPointF(rect.left(), rect.bottom()), QPointF(rect.left(), rect.top())),  # Gauche
    ]

    closest_point = None
    min_distance = float('inf')
    for line_start, line_end in lines:
        intersection = calculate_line_intersection(line_start, line_end, rect_pos, target_point)
        if intersection:
            distance = (intersection - target_point).manhattanLength()
            if distance < min_distance:
                min_distance = distance
                closest_point = intersection

    return closest_point

def calculate_line_intersection(p1, p2, p3, p4):
    denom = (p4.y() - p3.y()) * (p2.x() - p1.x()) - (p4.x() - p3.x()) * (p2.y() - p1.y())
    if denom == 0:
        return None  # Les lignes sont parallèles

    ua = ((p4.x() - p3.x()) * (p1.y() - p3.y()) - (p4.y() - p3.y()) * (p1.x() - p3.x())) / denom
    if 0 <= ua <= 1:
        intersection_x = p1.x() + ua * (p2.x() - p1.x())
        intersection_y = p1.y() + ua * (p2.y() - p1.y())
        return QPointF(intersection_x, intersection_y)
    return None

def calculate_circle_tangent(circle_center, circle_radius, target_point):
    dx = target_point.x() - circle_center.x()
    dy = target_point.y() - circle_center.y()
    distance = math.sqrt(dx * dx + dy * dy)

    if distance == 0:
        return QPointF(circle_center.x() + circle_radius, circle_center.y())

    scale = circle_radius / distance
    tangent_x = circle_center.x() + dx * scale
    tangent_y = circle_center.y() + dy * scale

    return QPointF(tangent_x, tangent_y)

def calculate_rectangle_middle_border(rect, rect_pos, target_point):
    rect = rect.translated(rect_pos)
    top_middle = QPointF((rect.left() + rect.right()) / 2, rect.top())
    bottom_middle = QPointF((rect.left() + rect.right()) / 2, rect.bottom())
    left_middle = QPointF(rect.left(), (rect.top() + rect.bottom()) / 2)
    right_middle = QPointF(rect.right(), (rect.top() + rect.bottom()) / 2)

    points = [top_middle, bottom_middle, left_middle, right_middle]
    closest_point = min(points, key=lambda point: (point - target_point).manhattanLength())

    return closest_point
