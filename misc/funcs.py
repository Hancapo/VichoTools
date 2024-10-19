import os
import xml.dom.minidom as md
from mathutils import Vector
import bpy
import string
import time
import uuid
import random

def export_milo_ymap_xml(ymapname, object, instance_name):

    bbmin, bbmax = get_bound_extents(object)

    root = md.Document()

    xml = root.createElement('CMapData')
    root.appendChild(xml)

    ymapName = root.createElement('name')
    ymapName.appendChild(root.createTextNode(
        os.path.basename(ymapname.split('.')[0])))
    xml.appendChild(ymapName)

    parent = root.createElement('parent')
    xml.appendChild(parent)

    flags = root.createElement('flags')
    flags.setAttribute('value', '0')
    xml.appendChild(flags)

    contentFlags = root.createElement('contentFlags')
    contentFlags.setAttribute('value', '9')
    xml.appendChild(contentFlags)

    streamingExtentsMin = root.createElement('streamingExtentsMin')
    streamingExtentsMin.setAttribute('x', str(bbmin[0] + 100))
    streamingExtentsMin.setAttribute('y', str(bbmin[1] + 100))
    streamingExtentsMin.setAttribute('z', str(bbmin[2] + 100))
    xml.appendChild(streamingExtentsMin)

    streamingExtentsMax = root.createElement('streamingExtentsMax')
    streamingExtentsMax.setAttribute('x', str(bbmax[0] + 100))
    streamingExtentsMax.setAttribute('y', str(bbmax[1] + 100))
    streamingExtentsMax.setAttribute('z', str(bbmax[2] + 100))
    xml.appendChild(streamingExtentsMax)

    entitiesExtentsMin = root.createElement('entitiesExtentsMin')
    entitiesExtentsMin.setAttribute('x', str(bbmin[0]))
    entitiesExtentsMin.setAttribute('y', str(bbmin[1]))
    entitiesExtentsMin.setAttribute('z', str(bbmin[2]))
    xml.appendChild(entitiesExtentsMin)

    entitiesExtentsMax = root.createElement('entitiesExtentsMax')
    entitiesExtentsMax.setAttribute('x', str(bbmax[0]))
    entitiesExtentsMax.setAttribute('y', str(bbmax[1]))
    entitiesExtentsMax.setAttribute('z', str(bbmax[2]))
    xml.appendChild(entitiesExtentsMax)

    entities = root.createElement('entities')

    Item = root.createElement('Item')
    Item.setAttribute('type', 'CMloInstanceDef')
    entities.appendChild(Item)

    archetypeName = root.createElement('archetypeName')
    archetypeName.appendChild(root.createTextNode(instance_name))
    Item.appendChild(archetypeName)

    itemFlags = root.createElement('flags')
    itemFlags.setAttribute('value', '1572865')
    Item.appendChild(itemFlags)

    itemGuid = root.createElement('guid')
    itemGuid.setAttribute('value', '0')
    Item.appendChild(itemGuid)

    itemPosition = root.createElement('position')
    itemPosition.setAttribute('x', str(object.location[0]))
    itemPosition.setAttribute('y', str(object.location[1]))
    itemPosition.setAttribute('z', str(object.location[2]))
    Item.appendChild(itemPosition)

    itemRotation = root.createElement('rotation')
    itemRotation.setAttribute(
        'x', str(object.rotation_euler.to_quaternion().x))
    itemRotation.setAttribute(
        'y', str(object.rotation_euler.to_quaternion().y))
    itemRotation.setAttribute(
        'z', str(object.rotation_euler.to_quaternion().z))
    itemRotation.setAttribute(
        'w', str(object.rotation_euler.to_quaternion().w))

    Item.appendChild(itemRotation)

    itemScaleXY = root.createElement('scaleXY')
    itemScaleXY.setAttribute('value', '1')
    Item.appendChild(itemScaleXY)

    itemScaleZ = root.createElement('scaleZ')
    itemScaleZ.setAttribute('value', '1')
    Item.appendChild(itemScaleZ)

    itemParentIndex = root.createElement('parentIndex')
    itemParentIndex.setAttribute('value', '-1')
    Item.appendChild(itemParentIndex)

    itemLodDist = root.createElement('lodDist')
    itemLodDist.setAttribute('value', '700')
    Item.appendChild(itemLodDist)

    itemchildLodDist = root.createElement('childLodDist')
    itemchildLodDist.setAttribute('value', '0')
    Item.appendChild(itemchildLodDist)

    itemlodLevel = root.createElement('lodLevel')
    itemlodLevel.appendChild(root.createTextNode('LODTYPES_DEPTH_ORPHANHD'))
    Item.appendChild(itemlodLevel)

    itennumChildren = root.createElement('numChildren')
    itennumChildren.setAttribute('value', '0')
    Item.appendChild(itennumChildren)

    itempriorityLevel = root.createElement('priorityLevel')
    itempriorityLevel.appendChild(root.createTextNode('PRI_REQUIRED'))
    Item.appendChild(itempriorityLevel)

    itemextensions = root.createElement('extensions')
    Item.appendChild(itemextensions)

    itemambientOcclusionMultiplier = root.createElement(
        'ambientOcclusionMultiplier')
    itemambientOcclusionMultiplier.setAttribute('value', '255')
    Item.appendChild(itemambientOcclusionMultiplier)

    itemartificialAmbientOcclusion = root.createElement(
        'artificialAmbientOcclusion')
    itemartificialAmbientOcclusion.setAttribute('value', '255')
    Item.appendChild(itemartificialAmbientOcclusion)

    itemtintValue = root.createElement('tintValue')
    itemtintValue.setAttribute('value', '0')
    Item.appendChild(itemtintValue)

    itemgroupId = root.createElement('groupId')
    itemgroupId.setAttribute('value', '0')
    Item.appendChild(itemgroupId)

    itemfloorId = root.createElement('floorId')
    itemfloorId.setAttribute('value', '0')
    Item.appendChild(itemfloorId)

    itemdefaultEntitySets = root.createElement('defaultEntitySets')
    Item.appendChild(itemdefaultEntitySets)

    itemnumExitPortals = root.createElement('numExitPortals')
    itemnumExitPortals.setAttribute('value', '0')
    Item.appendChild(itemnumExitPortals)

    itemMLOInstflags = root.createElement('MLOInstflags')
    itemMLOInstflags.setAttribute('value', '0')
    Item.appendChild(itemMLOInstflags)
    xml.appendChild(entities)

    xml_str = xml.toprettyxml(indent='\t')
    save_path = ymapname + '.xml'

    with open(save_path, 'w') as f:
        f.write(xml_str)
        f.close()


def get_bounds_from_single_object(obj):
    corners = []

    for pos in obj.bound_box:
        corners.append(Vector(pos))

    return corners


def get_bound_extents(obj, margin=0):
    corners = get_bounds_from_single_object(obj)

    if not corners:
        return Vector(), Vector()

    min = subtract_from_vector(get_min_vector_list(corners), margin)
    max = add_to_vector(get_max_vector_list(corners), margin)
    return min + obj.location, max + obj.location


def subtract_from_vector(v, f):
    r = Vector((0, 0, 0))
    r.x = v.x - f
    r.y = v.y - f
    r.z = v.z - f
    return r


def add_to_vector(v, f):
    r = Vector((0, 0, 0))
    r.x = v.x + f
    r.y = v.y + f
    r.z = v.z + f
    return r


def get_min_vector_list(vecs):
    x = []
    y = []
    z = []
    for v in vecs:
        x.append(v[0])
        y.append(v[1])
        z.append(v[2])
    return Vector((min(x), min(y), min(z)))


def get_max_vector_list(vecs):
    x = []
    y = []
    z = []
    for v in vecs:
        x.append(v[0])
        y.append(v[1])
        z.append(v[2])
    return Vector((max(x), max(y), max(z)))

def is_object_in_scene(obj):
    return obj.name in bpy.context.scene.collection.objects

def is_drawable_model(obj):
    return obj.sollum_type == 'sollumz_drawable_model'

def is_mesh(obj):
    return obj.type == 'MESH'

def is_drawable(obj):
    return obj.sollum_type == 'sollumz_drawable'

def gen_rdm_str(length=8):
    chars = string.ascii_letters + string.digits
    rd_part = ''.join(random.choice(chars) for _ in range(length))
    ts = str(int(time.time()))[-4:]
    uuid_str = str(uuid.uuid4()).replace('-', '')[:4]
    rdm_str = f"{rd_part}{ts}{uuid_str}"
    return rdm_str

def abs_path(path: str) -> str:
    return bpy.path.abspath(path)

def is_obj_in_any_collection(obj):
    return any(obj.name in collection.objects for collection in bpy.data.collections)