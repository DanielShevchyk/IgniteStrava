def create_activity_tags(activities_list):
    """
    Takes a list of activity dictionaries and creates Document tags for them.
    """
    #create source folder is required in this state
    #Change this to be dynamic at some point!@#!@#!@
    parent_path = "[default]Strava/Activities"
    
    system.tag.configure("[default]Strava", [{"name": "Activities", "tagType": "Folder"}], "m")
    
    tag_configs = []
    
    for activity in activities_list:
        # Name will be activity ID
        act_id = str(activity.get('id'))
        
        tag_def = {
            "name": act_id,
            "tagType": "AtomicTag",    # Standard tag type
            "dataType": "Document",    # Specifically for JSON
            "valueSource": "memory",   # We are writing to it
            "value": activity        # <--- Sets the value upon creation!
        }
        
        tag_configs.append(tag_def)
    
    print "Creating/Updating " + str(len(tag_configs)) + " tags"
    
    # collisionPolicy="o" (Overwrite) ensures that if the tag exists, 
    system.tag.configure(parent_path, tag_configs, "o")
    
    print "Tag generation done"