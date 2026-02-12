def create_activity_tags(activities_list):
    """
    Takes a list of activity dictionaries, creates Document tags for them,
    and updates a central Array tag with all Activity IDs.
    """
    if not activities_list:
        print "No activities to process."
        return
    
    parent_path = "[default]Strava/Activities"
    meta_parent_path = "[default]Strava/ActivitiesMetaData"
    id_array_tag_path = meta_parent_path + "/ArrayOfActivitiesID"
    
    # Ensure folder structures exist
    system.tag.configure("[default]Strava", [
        {"name": "Activities", "tagType": "Folder"},
        {"name": "ActivitiesMetaData", "tagType": "Folder"}
    ], "m")
    
    tag_configs = []
    all_ids = []
    
    for activity in activities_list:
       
        act_id_num = activity.get('id')
        act_id_str = str(act_id_num)
        
        
        all_ids.append(act_id_num)
        
        tag_def = {
            "name": act_id_str,
            "tagType": "AtomicTag",
            "dataType": "Document",
            "valueSource": "memory",
            "value": activity
        }
        
        tag_configs.append(tag_def)
    

    print "Creating/Updating " + str(len(tag_configs)) + " activity tags..."
    system.tag.configure(parent_path, tag_configs, "o")
    
    array_tag_config = [{
        "name": "ArrayOfActivitiesID",
        "tagType": "AtomicTag",
        "dataType": "Int8Array", 
        "valueSource": "memory"
    }]
    system.tag.configure(meta_parent_path, array_tag_config, "m")
    
    system.tag.writeBlocking([id_array_tag_path], [all_ids])
    
    print "Tag generation and ID Array update done. Total IDs: " + str(len(all_ids))