import bpy, math

bpy.types.Scene.height = bpy.props.FloatProperty(name = "Height", description="Height of each Turn", default = 0.0)
bpy.types.Scene.length = bpy.props.FloatProperty(name = "Length", description="Length of the Spring", default = 0.0)
bpy.types.Scene.frequency = bpy.props.FloatProperty(name = "Frequency", description="Number of Turns in the Spring", default = 0.0)
bpy.types.Scene.low_radius = bpy.props.FloatProperty(name = "Low Radius", description = "Smallest Radius in Helix", default = 0.0) 
bpy.types.Scene.high_radius = bpy.props.FloatProperty(name = "High Radius", description = "Largest Radius in Helix", default = 0.0) 
bpy.types.Scene.depth = bpy.props.FloatProperty(name = "Depth", description = "Depth of Helix when Beveled", default = 0.0) 


class HelixMakerPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Create"
    bl_label = "Add Helix"
    
    def draw(self, context):
        TheCol = self.layout.column(align=True)
        TheCol.operator("mesh.make_helix", text="Add Helix")
        
        row = self.layout.row(align=True)
        row.prop(context.scene, "height")
        
        row = self.layout.row(align=True)
        row.prop(context.scene, "length")  
        
        row = self.layout.row(align=True)
        row.prop(context.scene, "frequency") 
        
        row = self.layout.row(align=True)
        row.prop(context.scene, "low_radius") 
        
        row = self.layout.row(align=True)
        row.prop(context.scene, "high_radius") 

        row = self.layout.row(align=True)
        row.prop(context.scene, "depth") 
        
        
class MakeHelix(bpy.types.Operator):
    bl_idname = "mesh.make_helix"
    bl_label = "Add Helix"
    bl_options = {'UNDO'}
    
    def invoke(self, context, event):

        resolution = 20

        scene = bpy.data.scenes["Scene"]
        depth = (scene.depth * 0.0254) / 2
        
        num_turns = scene.length
        height_of_turn = scene.height * 0.0254
        freq= (1 + math.sqrt(scene.frequency)) / 2
        turn_radians = freq * 2*math.pi / num_turns
        bottom_radius = scene.low_radius * 0.0254
        upper_radius = scene.high_radius * 0.0254
        
        Vertices = []
        for i in range((int(num_turns)-1) * resolution + 1):
            position = i / float(resolution)

            angle = position * turn_radians

            curr_turn = position / float(num_turns - 1);
            
            width = upper_radius * math.exp(math.log(bottom_radius / upper_radius) * curr_turn)

            height = position * height_of_turn
            Vertices.append((-width * math.cos(angle), width*math.sin(angle), height))

        helix_attr = bpy.data.curves.new(name = 'HelixCurve', type = 'CURVE')      
        helix_attr.dimensions = '3D'
        helix_attr.fill_mode = 'FULL'
        helix_attr.bevel_depth = depth 
        helix_attr.bevel_resolution = 3
        group_verts = helix_attr.splines.new('POLY')
        group_verts.points.add(len(Vertices)-1)
        for i, (x, y, z) in enumerate(Vertices):  
            group_verts.points[i].co = (x, y, z, 1)
        helix_obj = bpy.data.objects.new('Helix', helix_attr)
        bpy.context.scene.objects.link(helix_obj)  
        
        return {'FINISHED'} 
    

def register():
    bpy.utils.register_class(MakeHelix)
    bpy.utils.register_class(HelixMakerPanel) 
    
register()