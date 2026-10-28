"""Install the public release's authored, image-free groundcover color mask.

Run explicitly inside Blender. Changes material nodes only; no mesh, animation,
sculpture, tree placement or camera modifications. Uses no reference pixels.
A zero-valued mask on the road material keeps the existing road shader clear.
"""
import bpy

TARGET_MATERIALS = (
    'PHOTO · Continuous pale olive earth and traced groundcover',
    'V11 Finish · Worn packed-earth streets',
    'V11 Landscape · Warm limestone soil mosaic',
    'V11 Landscape · Warm limestone soil mosaic · rock shoulder',
    'V12 Terrain · exposed limestone dry scrub and layered air',
)


def apply():
    report = []
    for name in TARGET_MATERIALS:
        material = bpy.data.materials.get(name)
        if material is None:
            raise RuntimeError('Required material not found: ' + name)
        nodes, links = material.node_tree.nodes, material.node_tree.links
        # On rerun reuse the authored replacement, keeping the operation idempotent.
        if nodes.get('Public release groundcover'):
            report.append({'material': name, 'status': 'already_installed'})
            continue
        candidates = [node for node in nodes if node.type == 'TEX_IMAGE'
                      and node.image and ('vegetation' in node.image.name.lower()
                                          or 'coverage mask' in node.image.name.lower())]
        if len(candidates) != 1:
            raise RuntimeError('Expected one coverage input in ' + name)
        old = candidates[0]
        destinations = [link.to_socket for link in links if link.from_node == old]
        if 'streets' in name.lower():
            output = nodes.new('ShaderNodeValue')
            output.outputs[0].default_value = 0.0
            mode = 'zero_on_road_surface'
        else:
            position = nodes.new('ShaderNodeNewGeometry')
            position.name = 'Public release world position'
            noise = nodes.new('ShaderNodeTexNoise')
            noise.name = 'Public release dry scrub noise'
            noise.noise_dimensions = '3D'
            noise.inputs['Scale'].default_value = 0.007
            noise.inputs['Detail'].default_value = 2.0
            noise.inputs['Roughness'].default_value = 0.7
            links.new(position.outputs['Position'], noise.inputs['Vector'])
            output = nodes.new('ShaderNodeValToRGB')
            output.color_ramp.interpolation = 'EASE'
            output.color_ramp.elements[0].position = 0.64
            output.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
            output.color_ramp.elements[1].position = 0.76
            output.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
            links.new(noise.outputs['Fac'], output.inputs['Fac'])
            mode = 'world_space_procedural_sparse_scrub'
        output.name = 'Public release groundcover'
        output.label = 'Reproducible image-free groundcover color mask'
        output.location = old.location
        for destination in destinations:
            links.new(output.outputs[0], destination)
        nodes.remove(old)
        material['Public groundcover'] = mode
        report.append({'material': name, 'status': 'installed', 'mode': mode})
    return report


if __name__ == '__main__':
    import json
    print(json.dumps(apply(), ensure_ascii=False, indent=2))
