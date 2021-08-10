# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

#  Autosaver add-on for Blender 2.81+
#  (c) 2021 Andrey Sokolov (so_records)

bl_info = {
    "name": "Autosaver",
    "author": "Andrey Sokolov",
    "version": (1, 0, 0),
    "blender": (2, 81, 0),
    "location": "Output Properties > Autosaver",
    "description": "Save copies of project before render",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Save"
}

import bpy, os, datetime
from bpy.props import StringProperty, BoolProperty
from bpy.types import Panel
from bpy.utils import register_class, unregister_class
from bpy.app.handlers import persistent
from shutil import copyfile

# ---------------------------- Operator Example  ---------------------------
    
@persistent
def atsv_save(self, context):
    sc = bpy.context.scene
    if not sc.autosaver_on:
        return
    if sc.autosaver == '':
        project_path = bpy.data.filepath
        project = bpy.path.basename(bpy.data.filepath)
        project_name = bpy.path.display_name_from_filepath(project_path)
        atsv_name = f'.{project_name}.autosaves'
        autosave_dir = project_path.replace(project, atsv_name)
        if not os.path.exists(autosave_dir):
            os.mkdir(autosave_dir)
        sc.autosaver = autosave_dir
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    project_path = bpy.data.filepath
    project_name = bpy.path.display_name_from_filepath(project_path)
    atsv_dir = sc.autosaver
    timing = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    new_path = os.path.join(atsv_dir, f"{project_name} {timing}.blend")
    copyfile(project_path, new_path)
    print(f"file saved: {new_path}")
    
# ---------------------------- Panel Example  ---------------------------
        
    
class AUTOSAVER_PT_Panel(Panel):
    bl_label = "Autosaver"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        sc = context.scene        
        col = layout.column(align = True)
        col.prop(sc, "autosaver_on", text = '')
        
    
    def draw(self, context):
        layout = self.layout
        sc = context.scene      
        col = layout.column(align = True)
        col.prop(sc, "autosaver", text = '')
        
        
classes = [
    AUTOSAVER_PT_Panel
]

def register():
    for cl in classes:
        register_class(cl)
    fp = ''
    bpy.types.Scene.autosaver = StringProperty(subtype="DIR_PATH", default = '')
    bpy.types.Scene.autosaver_on = BoolProperty(default=True)
    if atsv_save not in bpy.app.handlers.render_init:
        bpy.app.handlers.render_init.append(atsv_save)
    
def unregister():
    for cl in reversed(classes):
        unregister_class(cl)
    while atsv_save in bpy.app.handlers.render_init:
        bpy.app.handlers.render_init.remove(atsv_save)
        
if __name__ == '__main__':
    register() 