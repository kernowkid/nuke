import nuke
import eye

### Get filename and filetype  ###

p = nuke.Panel('PathBuilder')
p.addSingleLineInput('filename', '')
p.addEnumerationPulldown('filetype', '.exr .jpeg')
p.show()

filename =  p.value('filename')
filetype =  p.value('filetype')

### Get shot and version from eye  ###

nukePath = nuke.scriptName()
eye_resource = eye.get_resource_by_filename(nukePath)
facet_dict = eye_resource.get_facets()
shot = str(facet_dict['g3_name'])
version = 'v' + str(facet_dict['version']).zfill(3) 


## General render path build ###

from eyeplugins import p_nukepipe
foldername = p_nukepipe.get_nuke_render_dir() + '/' + filename + '/' + filename + '_' + shot + '_' + version + '.%04d' + filetype
foldername = foldername.replace('\\','/')


###build write node###
w = nuke.createNode('Write', inpanel=True)

#increment name
count = 1
while nuke.exists('AutoWrite' + str(count)):
    count += 1

w.knob('name').setValue('AutoWrite' + str(count))
w.knob('file').setValue(foldername)





eye_resource = eye.get_resource_by_filename(nukePath)
facet_dict = eye_resource.get_facets()
import pprint

pprint.pprint(facet_dict)
print facet_dict[g3_name]

