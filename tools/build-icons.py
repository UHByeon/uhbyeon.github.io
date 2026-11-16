"""Render terminal favicon PNG/ICO fallbacks with the Python standard library."""
from pathlib import Path
import math
import struct
import zlib

ROOT = Path(__file__).resolve().parent.parent
BG = (16,20,26)
GREEN = (91,240,108)


def distance_segment(x,y,x1,y1,x2,y2):
    dx,dy=x2-x1,y2-y1
    t=max(0,min(1,((x-x1)*dx+(y-y1)*dy)/(dx*dx+dy*dy)))
    return math.hypot(x-(x1+t*dx),y-(y1+t*dy))


def inside_round(x,y,left,top,right,bottom,radius):
    cx=min(max(x,left+radius),right-radius)
    cy=min(max(y,top+radius),bottom-radius)
    return math.hypot(x-cx,y-cy)<=radius


def sample(x,y):
    if not inside_round(x,y,0,0,32,32,5): return (0,0,0,0)
    outer=inside_round(x,y,3,4.5,29,27.5,3)
    inner=inside_round(x,y,5,6.5,27,25.5,1)
    prompt=min(distance_segment(x,y,*segment) for segment in ((9,12,13,16),(13,16,9,20),(17,20,23,20)))<=1
    return (*(GREEN if (outer and not inner) or prompt else BG),255)


def chunk(kind,data):
    return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)


def png(size):
    scale=4
    data=bytearray()
    for y in range(size):
        data.append(0)
        for x in range(size):
            sums=[0,0,0,0]
            for sy in range(scale):
                for sx in range(scale):
                    color=sample((x+(sx+.5)/scale)*32/size,(y+(sy+.5)/scale)*32/size)
                    for c in range(4): sums[c]+=color[c]
            data.extend(round(v/(scale*scale)) for v in sums)
    header=struct.pack('>IIBBBBB',size,size,8,6,0,0,0)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',header)+chunk(b'IDAT',zlib.compress(bytes(data),9))+chunk(b'IEND',b'')


sizes=(16,32,48)
images=[png(size) for size in sizes]
offset=6+16*len(sizes)
entries=[]
for size,image in zip(sizes,images):
    entries.append(struct.pack('<BBBBHHII',size,size,0,0,1,32,len(image),offset))
    offset+=len(image)
(ROOT/'favicon.ico').write_bytes(struct.pack('<HHH',0,1,len(sizes))+b''.join(entries)+b''.join(images))
(ROOT/'favicon-32.png').write_bytes(images[1])
(ROOT/'apple-touch-icon.png').write_bytes(png(180))
print('Created terminal icons: ICO (16/32/48), PNG (32), touch icon (180).')
