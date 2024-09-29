##########################################################
# These callbacks are to be set as values for the
# "beforRender" and "afterRender" knobs on the Write node.
# The suplied Write node template already have these.
# Providing this file for visibility and easy editing.
##########################################################

##########################################################
# beforeRender

import nuke

# Save script
nuke.scriptSave()

# Prepare EXR Metadata values
script_name = nuke.root()['name'].value()
openclip = nuke.thisNode()['openclip'].value()
nuke_version = nuke.env['NukeVersionString']

metadata_dict = {
'nuke_version': '{remove nuke_version}',
'nuke_script': '{remove nuke_script}',
'flame/openclip': '{flame/openclip}',
'nuke_version': '{set nuke_version "'+nuke_version+'" }',
'nuke_script': '{set nuke_script "'+script_name+'" }',
'flame/openclip': '{set flame/openclip "'+openclip+'"}'
}

# Set EXR Metadata
try:
    metadata_node = nuke.thisNode().input(0)
    meta_keys = []
    for k, v in metadata_dict.items():
        meta_keys.append(v)
        metadata_node['metadata'].fromScript("\n".join(meta_keys))
except:
    pass

nuke.scriptSave()

# End beforeRender
##########################################################

##########################################################
# afterRender

import nuke
import re
import subprocess

# Get this write node
node = nuke.thisNode()

# Get the openclip file from the metadata
openclip = node.metadata()['flame/openclip']

# Get the render path from write node and change the frame string to a single frame
filename = node['file'].value()
frame_pattern = r'(%\d{0,4}d|#|#{2,}|[0-9]{4})(?![-_/])'
first_frame = str(int(nuke.root()['first_frame'].value())).zfill(4)
filename = re.sub(frame_pattern, first_frame, filename)
print(filename)

# Path to Python. Need the PyYAML module installed
python_path = node['python_exec'].value()
update_openclip_path = node['update_openclip_script'].value()

# Process the clip
process = subprocess.Popen(
    [python_path, update_openclip_path, '-f', openclip, '-i', filename],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
stdout, stderr = process.communicate()
if stderr:
    print("Error:", stderr.decode('utf-8'))

# End afterRender
##########################################################
