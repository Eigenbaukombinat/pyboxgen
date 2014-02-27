from dxfwrite import DXFEngine as dxf

fn = 'kast.dxf'
drawing = dxf.drawing(fn)


class Kasten(object):

    def __init__(self, b, t, h, dis, das, df):
        self.b = b
        self.t = t
        self.h = h
        self.x_off = 0
        self.y_off = 0
        self.dis = dis
        self.das = das
        self.df = df
        self.drawing = dxf.drawing('kast.dxf')
        self.drawing.add_layer('LINES')
        self.hori_schlitze = []
        self.vert_schlitze = []

    def save(self):
        self.drawing.save()

    def l(self, sx, sy, ex, ey):
        sx = sx + self.x_off
        sy = sy + self.y_off
        ex = ex + self.x_off
        ey = ey + self.y_off
        self.drawing.add(dxf.line((sx, sy), (ex, ey), layer='LINES'))

    def rd(self, sx, sy, ex, ey):
        """rechteck durch diagonale"""
        self.l(sx, sy, ex, sy)
        self.l(sx, sy, sx, ey)
        self.l(ex, sy, ex, ey)
        self.l(ex, ey, sx, ey)

    def rs(self, sx, sy, x, y):
        """rechteck durch start, x,y-laengen"""
        self.l(sx, sy, x + sx, sy)
        self.l(sx, sy, sx, sy + y)
        self.l(sx + x, sy, sx + x, sy + y)
        self.l(sx + x, sy + y, sx, sy + y)

    def hk(self, sx, sy, ex, ey):
        """halbkreis von sx, xy nach ex, ey, im uhrzeigersinn"""
        if sx == ex:
            cx = sx
            rp = (sy, ey)
            if sy > ey:
                sa = 270
                ea = 90
                cy = sy - ((sy - ey) / 2.0)
            else:
                sa = 90
                ea = 270
                cy = sy + ((ey - sy) / 2.0)
        elif sy == ey:
            cy = sy
            rp = (sx, ex)
            if sx > ex:
                sa = 0
                ea = 180
                cx = sx - ((sx - ex) / 2.0)
            else:
                sa = 180
                ea = 360
                cx = sx + ((ex - sx) / 2.0)
        else:
            raise ValueError("Halbkreis failed!")
        radius = abs(rp[0] - rp[1]) / 2.0
        cx = cx + self.x_off
        cy = cy + self.y_off
        self.drawing.add(dxf.arc(radius=radius, center=(cx, cy),
                                 startangle=sa, endangle=ea, layer='LINES'))

    def vert_schlitz(self, x):
        t = self.t
        dis = self.dis
        das = self.das
        df = self.df
        x = x - (dis / 2.0)
        y_before = 0
        for i, y in enumerate(self.hori_schlitze + [t - (dis / 2.0)]):
            if i == 0:
                ysd = das
            else:
                ysd = dis / 2.0
            if i == len(self.hori_schlitze):
                yed = das - (dis / 2.0)
            else:
                yed = dis / 2.0
            self.l(x, y_before + ysd,
                   x, y - yed)
            self.l(x + dis, y_before + ysd,
                   x + dis, y - yed)
            y_before = y

        self.hk(x, das,
                x + df, das)
        self.hk(x + dis - df, das,
                x + dis, das)
        self.l(x + df, das,
               x + dis - df, das)
        self.hk(x + df, t - das,
                x, t - das)
        self.hk(x + dis, t - das,
                x + dis - df, t - das)
        self.l(x + df, t - das,
               x + dis - df, t - das)

    def seit_schlitz(self, x):
        dis = self.dis
        h = self.h - (2 * dis)
        das = self.das
        df = self.df
        x = x - dis/2.0
        self.l(x, h/4.0 + 2*dis,x, h - h/4.0 + 2*dis)
        self.l(x + dis, h/4.0 + 2*dis, x + dis, h - h/4.0 + 2*dis)
        self.hk(x, h/4.0 + 2*dis,
                x + df, h/4.0 + 2*dis)
        self.hk(x + dis - df, h/4.0 + 2*dis,
                x + dis, h/4.0 + 2*dis)
        self.l(x + df, h/4.0 + 2*dis,
               x + dis - df, h/4.0 + 2*dis)
        self.hk(x + df, h - h/4.0 + 2*dis,
                x, h - h/4.0 + 2*dis)
        self.hk(x + dis, h - h/4.0 + 2*dis,
                x + dis - df, h - h/4.0 + 2*dis)
        self.l(x + df, h - h/4.0 + 2*dis,
               x + dis - df, h - h/4.0 + 2*dis)

    def hori_schlitz(self, y):
        b = self.b
        dis = self.dis
        das = self.das
        df = self.df
        y = y - (dis / 2.0)
        x_before = 0
        for i, x in enumerate(self.vert_schlitze + [b - (dis / 2.0)]):
            if i == 0:
                xsd = das
            else:
                xsd = dis / 2.0
            if i == len(self.vert_schlitze):
                xed = das - (dis / 2.0)
            else:
                xed = dis / 2.0
            self.l(x_before + xsd, y,
                   x - xed, y)
            self.l(x_before + xsd, y + dis,
                   x - xed, y + dis)
            x_before = x

        self.hk(das, y,
                das, y + df)
        self.l(das, y + df,
               das, y + dis - df)
        self.hk(das, y + dis - df,
                das, y + dis)
        self.l(b - das, y + df,
                b - das, y + dis - df)
        self.hk(b - das, y + df,
                b - das, y)
        self.hk(b - das, y + dis,
                b - das, y + dis - df)


    def bodenplatte(self):
        self.rs(0 + (self.das / 2.0),
                0 + (self.das / 2.0),
                self.b - self.das,
                self.t - self.das)
        for x in self.vert_schlitze:
            self.vert_schlitz(x)
        for y in self.hori_schlitze:
            self.hori_schlitz(y)

    def breitseite(self, mirror_schlitze=False):
        das = self.das
        self.l(0, 0, self.b, 0)
        self.l(0, self.h, self.b, self.h)
        #links
        self.l(0,0, 0, self.h /3.0)
        self.l(0, self.h/3.0, das - self.df, self.h/3.0)
        self.hk(das - self.df, self.h/3.0, das, self.h/3.0)
        self.l(das, self.h/3.0, das, self.h/3.0*2.0)
        self.hk(das, self.h/3.0*2.0, das - self.df, self.h/3.0*2.0)
        self.l(das - self.df, self.h/3.0*2.0, 0, self.h/3.0*2.0)
        self.l(0,self.h/3.0*2.0, 0, self.h)
        #rechts
        self.l(self.b,0, self.b, self.h /3.0)
        self.l(self.b, self.h/3.0, self.b-das + self.df, self.h/3.0)
        self.hk(self.b-das, self.h/3.0, self.b-das + self.df, self.h/3.0)
        self.l(self.b-das, self.h/3.0, self.b-das, self.h/3.0*2.0)
        self.hk( self.b - das + self.df, self.h/3.0*2.0, self.b-das, self.h/3.0*2.0)
        self.l(self.b - das + self.df, self.h/3.0*2.0, self.b, self.h/3.0*2.0)
        self.l(self.b,self.h/3.0*2.0, self.b, self.h)
        if mirror_schlitze:
            schlitze = [self.b-sch for sch in self.vert_schlitze]
        else:
            schlitze = self.vert_schlitze

        self.seiten(self.b, schlitze)

    def tiefseite(self, mirror_schlitze=False):
        das = self.das
        t = self.t
        h = self.h
        self.l(das, 0, self.t - das, 0)
        self.l(das, self.h, self.t-das, self.h)
        #rechts
        self.l(t-das,0, t-das, self.h /3.0)
        self.l(t-das+self.df, self.h/3.0, t - das + self.df, self.h/3.0)
        self.hk(t-das+self.df, self.h/3.0,t - das, self.h/3.0)
        self.l(t, self.h/3.0, t, self.h/3.0*2.0)
        self.hk(t-das, self.h/3.0*2.0, t - das+self.df, self.h/3.0*2.0)
        self.l( t - das+self.df, self.h/3.0*2.0, t, self.h/3.0*2.0)
        self.l(t - das+self.df, self.h/3.0, t, self.h/3.0)
        self.l(t - das,self.h/3.0*2.0, t - das, self.h)
        #links
        self.l(das,0, das, self.h /3.0)
        self.l(das-self.df, self.h/3.0, 0, self.h/3.0)
        self.hk(das, self.h/3.0, das-self.df, self.h/3.0)
        self.l(das-das, self.h/3.0, das-das, self.h/3.0*2.0)
        self.hk(das-self.df, self.h/3.0*2.0,das, self.h/3.0*2.0)
        self.l(0, self.h/3.0*2.0, das-self.df, self.h/3.0*2.0)
        self.l(das,self.h/3.0*2.0, das, self.h)
        if mirror_schlitze:
            schlitze = [t-sch for sch in self.hori_schlitze]
        else:
            schlitze = self.hori_schlitze

        self.seiten(self.t, schlitze)

    def seiten(self, l, sch):
        df = self.df
        dis = self.dis
        b = l
        das  = self.das
        self.l(das/2.0, dis, b - das / 2.0, dis)
        self.l(das/2.0, 2*dis, b - das / 2.0, 2*dis)

        self.hk(das/2.0, dis, das/2.0, dis+df)
        self.l(das/2.0, dis + df, das/2.0, (2 * dis) - df)
        self.hk(das/2.0, (2 * dis) - df, das / 2.0, 2 * dis)

        self.hk(b - das/2.0, dis + df, b - das/2.0, dis)
        self.l(b - das/2.0, dis + df, b - das /2.0, (2*dis) - df)
        self.hk(b - das/2.0, 2*dis, b - das / 2.0, 2 * dis - df)
        for x in sch:
            self.seit_schlitz(x)

    def teile(self, b, andere_schlitze, yoffset=False):
        dis = self.dis
        das = self.das
        h = self.h - (2 * dis)
        yoff = 0
        if yoffset:
            yoff = -(dis / 2.0)

        df = self.df
        #unten h
        self.l(das, 0 - dis/2.0,
               b - das, 0 - dis/2.0)
        #links v
        self.l(das, 0-dis/2.0,
               das, h / 4.0 + yoff)
        self.hk(das, h / 4.0 + yoff,
                das - df, h / 4.0 + yoff)
        self.l(das - df, h / 4.0 + yoff,
               das / 2.0, h / 4.0 + yoff)
        self.hk(das - df, h - (h / 4.0) + yoff,
                das, h - (h / 4.0) + yoff)
        self.l(das - df, h - (h / 4.0) + yoff,
               das / 2.0, h - (h / 4.0) + yoff)
        self.l(das / 2.0, h - (h / 4.0) + yoff,
               das / 2.0, h / 4.0 + yoff)
        self.l(das, h - (h / 4.0) + yoff,
               das, h)

        #rechts v
        self.l(b - das, 0 - dis/2.0,
               b - das, h / 4.0 + yoff)
        self.hk(b - das + df, h / 4.0 + yoff,
                b - das, h / 4.0 + yoff)
        self.l(b - das + df, h / 4.0 + yoff,
               b - (das / 2.0), h / 4.0 + yoff)
        self.hk(b - das, h - (h / 4.0) + yoff,
                b - das + df, h - (h / 4.0) + yoff)
        self.l(b - das + df, h - (h / 4.0) + yoff,
               b - (das / 2.0), h - (h / 4.0) + yoff)
        self.l(b - (das / 2.0), h - (h / 4.0) + yoff,
               b - (das / 2.0), h / 4.0 + yoff)
        self.l(b - das, h - (h / 4.0) + yoff,
               b - das, h)
        x_before = 0
        for i, x in enumerate(andere_schlitze + [b - (dis / 2.0)]):
            x = x + (dis / 2.0)
            if i == 0:
                x_start = x_before + das
            else:
                x_start = x_before + dis
            if i == len(andere_schlitze):
                x_end = x - das
            else:
                x_end = x - dis
            self.l(x_start, h,
                   x_end, h)
            if i != len(andere_schlitze):
                self.l(x - dis, h,
                       x - dis, (h / 2.0) - (df / 2.0))
                self.hk(x - dis, (h / 2.0) - (df / 2.0),
                       x - dis + df, (h / 2.0) - (df / 2.0))
                self.hk(x - df,  (h / 2.0) - (df / 2.0),
                       x, (h / 2.0) - (df / 2.0))
                self.l(x - dis + df, (h / 2.0) - (df / 2.0),
                       x - df,      (h / 2.0) - (df / 2.0))
                self.l(x,       (h / 2.0) - (df / 2.0),
                       x,       h)
            x_before = x - dis

    def hori_teile(self):
        self.teile(self.b, self.vert_schlitze)

    def vert_teile(self):
        self.teile(self.t, self.hori_schlitze, True)

b=460
t=560
h=70
dis=5
das=5
df=2
hs = [140, 280]
vs = [115, 230]

test = Kasten(b, t, h, dis, das, df)
test.hori_schlitze = hs
test.vert_schlitze = vs
test.bodenplatte()
test.x_off = b + 15
for x in range(len(test.hori_schlitze)):
    test.hori_teile()
    test.y_off += h+15
for x in range(len(test.vert_schlitze)):
    test.vert_teile()
    test.y_off += h+15
test.breitseite()
test.y_off += h+15
test.tiefseite()
test.y_off += h+15
test.breitseite(True)
test.y_off += h+15
test.tiefseite(True)





test.save()
