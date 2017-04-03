## init.py
## loaded by nuke before menu.py

# to add a folder inside the '.nuke' folder -> nuke.pluginAddPath('./myFolder')

nuke.pluginAddPath('./python')
nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./icons')

## create autowrite directories 
def createWriteDir():
    import nuke, os, errno
    file = nuke.filename(nuke.thisNode())
    dir = os.path.dirname( file )
    osdir = nuke.callbacks.filenameFilter( dir )
    # cope with the directory existing already by ignoring that exception
    try:
      os.makedirs( osdir )
    except OSError, e:
      if e.errno != errno.EEXIST:
        raise
nuke.addBeforeRender(createWriteDir)


def createWritePath():
    import nuke
    import eye
    
    wn = nuke.thisNode()
    
    ### Get filename and filetype  ###
    filename =  wn.name()
    
    ### test if file type is set. if not set filetype  'exr' ###
    filetype = ''
    exttest = wn['file_type'].getValue()
    if exttest == 0:
        filetype = '.exr'
    else:
        filetype = '.' + str(wn['file_type'].value())

    ### Get shot and version from eye  ###
    nukePath = nuke.scriptName()

    try:
        eye_resource = eye.get_resource_by_filename(nukePath)
    except eye.EyeNotFoundError:
        nuke.message("You need to have an open file")
        return      
    
    facet_dict = eye_resource.get_facets()
    shot = str(facet_dict['g3_name'])
    version = 'v' + str(facet_dict['version']).zfill(3) 
    
    ## build render path ###
    from eyeplugins import p_nukepipe
    renderdir = p_nukepipe.get_nuke_render_dir() 
    
    renderpath = ''
    
    if filetype == '.mov':
        renderpath =  renderdir + '/' + filename + '/' + filename + '_' + shot + '_' + version  + filetype
    else:
        renderpath =  renderdir + '/' + filename + '/' + filename + '_' + shot + '_' + version + '.%04d' + filetype    
    
    renderpath = renderpath.replace('\\','/')
    
    ### set write nodes file knob
    wn.knob('file').setValue(renderpath)
    

nuke.addKnobChanged(createWritePath, nodeClass = 'Write')
