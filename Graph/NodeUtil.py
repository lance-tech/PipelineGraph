from enum import Enum

LEFT_PORT = 'INPUT'
RIGHT_PORT = 'OUTPUT'

class NODE_TYPE(Enum):
    art = 0
    mod = 1
    trk = 2
    rig = 3
    tex = 4
    shd = 5
    ani = 6
    vfx = 7
    cfx = 8
    lgt = 9
    render = 10
    roto = 12
    mat = 13
    cmp = 14
    user = 15
    file = 16


class NODE_COLOR(Enum):
    art = (245, 174, 21, 255)
    mod = (142, 142, 142, 255)
    trk = (220, 30, 30, 255)
    rig = (27, 27, 27, 255)
    tex = (228, 228, 228, 255)
    shd = (107, 107, 107, 255)
    ani = (150, 18, 18, 255)
    vfx = (171, 74, 9, 255)
    cfx = (122, 101, 141, 255)
    lgt = (244, 242, 112, 255)
    render = (62, 62, 154, 255)
    roto = (18, 214, 46, 255)
    mat = (18, 214, 46, 255)
    cmp = (37, 170, 186, 255)
    user = (212, 208, 169, 255)
    file = (107, 107, 107, 255)


def getNodeInitialData(_type):
    if _type == NODE_TYPE.art:
        return {'name': 'Art', 'color': NODE_COLOR.art}
    elif _type == NODE_TYPE.mod:
        return {'name': 'Modeling', 'color': NODE_COLOR.mod}
    elif _type == NODE_TYPE.tex:
        return {'name': 'Texture', 'color': NODE_COLOR.tex}
    elif _type == NODE_TYPE.shd:
        return {'name': 'Shader', 'color': NODE_COLOR.shd}
    elif _type == NODE_TYPE.rig:
        return {'name': 'Rigging', 'color': NODE_COLOR.rig}
    elif _type == NODE_TYPE.ani:
        return {'name': 'Animation', 'color': NODE_COLOR.ani}
    elif _type == NODE_TYPE.trk:
        return {'name': 'Tracking', 'color': NODE_COLOR.trk}
    elif _type == NODE_TYPE.vfx:
        return {'name': 'VFX', 'color': NODE_COLOR.vfx}
    elif _type == NODE_TYPE.cfx:
        return {'name': 'CFX', 'color': NODE_COLOR.cfx}
    elif _type == NODE_TYPE.lgt:
        return {'name': 'Lighting', 'color': NODE_COLOR.lgt}
    elif _type == NODE_TYPE.render:
        return {'name': 'Rendering', 'color': NODE_COLOR.render}
    elif _type == NODE_TYPE.roto:
        return {'name': 'Roto', 'color': NODE_COLOR.roto}
    elif _type == NODE_TYPE.mat:
        return {'name': 'Matte', 'color': NODE_COLOR.mat}
    elif _type == NODE_TYPE.cmp:
        return {'name': 'Composite', 'color': NODE_COLOR.cmp}