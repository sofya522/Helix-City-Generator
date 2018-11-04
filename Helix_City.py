import bpy, math
import random 

#helix formation parameters, parameters for for city generation, and landscape generation 
bpy.types.Scene.height = bpy.props.FloatProperty(name = "Height", description="Height of each Turn", default = 0.0)
bpy.types.Scene.length = bpy.props.FloatProperty(name = "Length", description="Length of the Spring", default = 0.0)
bpy.types.Scene.frequency = bpy.props.FloatProperty(name = "Frequency", description="Number of Turns in the Spring", default = 0.0)
bpy.types.Scene.low_radius = bpy.props.FloatProperty(name = "Low Radius", description = "Smallest Radius in Helix", default = 0.0) 
bpy.types.Scene.high_radius = bpy.props.FloatProperty(name = "High Radius", description = "Largest Radius in Helix", default = 0.0) 
bpy.types.Scene.depth = bpy.props.FloatProperty(name = "Depth", description = "Depth of Helix when Beveled", default = 0.0) 
bpy.types.Scene.create_city = bpy.props.BoolProperty(name = "Add City", description = "Generate a City based on Helix", default = False)
bpy.types.Scene.density = bpy.props.FloatProperty(name = "Density", description = "Density of buildings in generated city", default = 0.0) 
bpy.types.Scene.add_landscape = bpy.props.BoolProperty(name = "Add Landscape", description = "Create a Landscape along the helix", default = False)

#function to add specified buildings to helix (at least one building should be active for this function to work properly) 
def generate_city(positions, density):
    buildings = [] 
    #FRAME = 0 
    for index in range(len(bpy.data.objects)):
        
        if 'House' in bpy.data.objects[index].name:
            buildings.append(bpy.data.objects[index])
    
    num_buildings = len(buildings)
    
    if num_buildings == 0:
        print("Add more buildings and THEN try!") 
        return  
    
    for p in range(0, len(positions), int (density)):
        
        b_index  = random.randint (0, num_buildings-1)
        curr_building = buildings[b_index]
        bpy.context.scene.objects.active = curr_building
        print(bpy.context.scene.objects.active)
        bpy.ops.object.duplicate_move()
    
    #bpy.context.scene.frame_set(FRAME)
    
    duplicates = []
    for i in range (len(bpy.data.objects)):
        house_ind = random.randint(1, 3)
        print(house_ind)
        house_name = 'House_' + str(int(house_ind))
        print(house_name)
        if house_name in bpy.data.objects[i].name:
            duplicates.append(bpy.data.objects[i])
    #        bpy.data.objects[i].keyframe_insert(data_path="location")
    
    scale_max = 0.0001
    print (len(duplicates))
    for pos in range(0, len(positions), int (density)):
        dup_ind = random.randint(0, len(duplicates)-1)
        duplicates[dup_ind].location = (positions[pos].co.x, positions[pos].co.y, positions[pos].co.z)
        scale_fact = random.uniform(0.0, scale_max)
        #duplicates[dup_ind].scale = (duplicates[dup_ind].scale[0] + scale_max, duplicates[dup_ind].scale[1] + scale_max, duplicates[dup_ind].scale[2] + scale_max)
        duplicates[dup_ind].rotation_euler = (duplicates[dup_ind].rotation_euler[0], duplicates[dup_ind].rotation_euler[1], duplicates[dup_ind].rotation_euler[2] + random.randint(0,360)) 
     #   duplicates[dup_ind].keyframe_insert(data_path = "location")
        #duplicates[dup_ind].keyframe_insert(data_path = "scale")
    #    duplicates[dup_ind].keyframe_insert(data_path = "rotation_euler")
      #  FRAME = FRAME + 1 
       # bpy.context.scene.frame_set(FRAME)
        scale_max += 0.00005

#adds a landscape based on the type of helix added by the user (onlyif "Add Landscape" boolean is true)
def add_landscape(helix):
    scene = bpy.data.scenes["Scene"] 
    print ("Give the city a landscape/mountainous base.")
    bpy.ops.mesh.landscape_add(random_seed = 3, refresh=True)
    land_name = "Landscape"
    for obj in bpy.data.objects:
        if land_name in obj.name: 
            land = obj
    bottom_radius = scene.low_radius * 0.0254
    upper_radius = scene.high_radius * 0.0254
#    FRAME = 0 
#    bpy.context.scene.frame_set(FRAME)
#    bpy.context.scene.frame_set(FRAME)
    if land:
        
 #       land.keyframe_insert(data_path = "scale")
  #      FRAME += 80
   #     bpy.context.scene.frame_set(FRAME)
        land.dimensions = helix.dimensions 
        land.scale[2] += 0.7
        land.scale[0] -= 0.1
        land.scale[1] -= 0.1
    #    land.keyframe_insert(data_path = "scale")
        print(helix.dimensions[2])
        print (land.scale[2])
        land.location = (0.0, 0.0, 0.0)
        
#UI for helix, city, and landscape creation 
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
        
        row = self.layout.row(align=True)
        row.prop(context.scene, "create_city") 
        
        row = self.layout.row(align=True)
        row.prop(context.scene, "density") 
        
        row = self.layout.row(align=True)
        row.prop(context.scene, "add_landscape") 
        
#adds a strong bevel to the helix curve to make it present in the render 
def create_wall(cube, verts):
    helix = bpy.data.objects["Helix"]
    modifier = cube.modifiers.new(name="Array", type='ARRAY')
    modifier.fit_type = 'FIT_CURVE'
    modifier.curve = helix
    modifier_1 = cube.modifiers.new(name="curve", type='CURVE')
    modifier_1.object = helix
#    FRAME = 0
    cube.scale = (0, 0, 0)
    #cube.keyframe_insert(data_path = "scale")
 #   bpy.context.scene.frame_set(FRAME)
    
    for i in range (5):
        cube.scale[0] += 0.2
        cube.scale[1] += 0.2
        cube.scale[2] += 0.2
  #      cube.keyframe_insert(data_path = "scale")
#        FRAME = FRAME + 20
#        bpy.context.scene.frame_set(FRAME)
        
    print("make wall")
    
    
#function that creates helix (if you only need this functionality, this basic script for that is also in the repository 
class MakeHelix(bpy.types.Operator):
    bl_idname = "mesh.make_helix"
    bl_label = "Add Helix"
    bl_options = {'UNDO'}
    
    def invoke(self, context, event):

        resolution = 30

        scene = bpy.data.scenes["Scene"]
        depth = (scene.depth * 0.0254) / 2
        
        num_turns = scene.length
        height_of_turn = scene.height * 0.0254
        freq= (1 + math.sqrt(scene.frequency)) / 2
        turn_radians = freq * 2*math.pi / num_turns
        bottom_radius = scene.low_radius * 0.0254
        upper_radius = scene.high_radius * 0.0254
        count = 0
        total_height = 0
        
        Vertices = []
        for i in range((int(num_turns)-1) * resolution + 1):
            position = i / float(resolution)

            angle = position * turn_radians

            curr_turn = position / float(num_turns - 1);
             
            width = upper_radius * math.exp(math.log(bottom_radius / upper_radius) * curr_turn)

            height = position * height_of_turn
            total_height += height_of_turn
            Vertices.append((-width * math.cos(angle), width*math.sin(angle), height))
            count += 1
        helix_attr = bpy.data.curves.new(name = 'HelixCurve', type = 'CURVE')      
        helix_attr.dimensions = '3D'
        helix_attr.fill_mode = 'FULL'
        helix_attr.bevel_depth = depth 
        helix_attr.bevel_resolution = 3
        group_verts = helix_attr.splines.new('POLY')
        group_verts.points.add(len(Vertices)-1)
        last_vert = (0,0,0)
        for i, (x, y, z) in enumerate(Vertices):  
            group_verts.points[i].co = (x, y, z, 1)
            if i == 0: 
                last_vert = (x, y, z)
        
        
        
        helix_obj = bpy.data.objects.new('Helix', helix_attr)
        bpy.context.scene.objects.link(helix_obj)  
        if scene.create_city == True:
            generate_city(group_verts.points, scene.density)
        if scene.add_landscape == True:
            add_landscape(helix_obj)
            
        
        #bpy.ops.mesh.primitive_cube_add(radius=0.02, location = last_vert)
        #create_wall(bpy.context.object, Vertices)
            
        return {'FINISHED'} 


def register():
    bpy.utils.register_class(MakeHelix)
    bpy.utils.register_class(HelixMakerPanel) 
    
register()