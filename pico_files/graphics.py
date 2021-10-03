import math
import framebuf as fb

class Graphics():
    def __init__(self, width, height, pixel, hline, vline, text):
        self.width = width
        self.height = height
        self._pixel = pixel
        self.hline = hline
        self.vline = vline
        self.base_text = text

    def fill_rect(self, x0, y0, width, height, *args, **kwargs):
        if y0 < -height or y0 > self.height or x0 < -width or x0 > self.width:
            return
        for i in range(x0, x0+width):
            self.vline(i, y0, height, *args, **kwargs)

    def line(self, x0, y0, x1, y1, *args, **kwargs):
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx // 2
        ystep = 0
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1
        while x0 <= x1:
            if steep:
                self._pixel(y0, x0, *args, **kwargs)
            else:
                self._pixel(x0, y0, *args, **kwargs)
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            x0 += 1

    def base_text(self, string, x, y, col, *args, **kwargs):
        self.text(s=string, x=x, y=y, c=col, *args, **kwargs)

class Shapes():
    @staticmethod
    def poly_lines(args):
        pts = [int(coord) for tup in args for coord in tup]
        lines = []
        for pt in range(0, len(pts), 2):
            a = pt % (len(pts))
            b = (pt+1) % (len(pts))
            c = (pt+2) % (len(pts))
            d = (pt+3) % (len(pts))

            lines.append((pts[a], pts[b], pts[c], pts[d]))
        return lines

    @staticmethod
    def unpack_poly(poly):
        return [coord for tup in poly for coord in tup]

    @staticmethod
    def contains(poly, point):
        pts = [int(coord) for tup in poly for coord in tup]

        x_pts = pts[::2]
        y_pts = pts[1::2]

        min_x = min(x_pts)
        min_y = min(y_pts)
        max_x = max(x_pts)
        max_y = max(y_pts)


        xfit = point[0] > min_x and point[0] < max_x
        yfit = point[1] > min_y and point[1] < max_y

        return xfit and yfit
