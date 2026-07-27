import PySpin

def configure_chunk_data(nodemap):
    """Enables chunk mode and the specific ImageTimestamp chunk on the camera."""
    # 1. Activate Chunk Mode
    node_chunk_mode = PySpin.CBooleanPtr(nodemap.GetNode("ChunkModeActive"))
    if PySpin.IsWritable(node_chunk_mode):
        node_chunk_mode.SetValue(True)
    
    # 2. Select ImageTimestamp
    node_chunk_selector = PySpin.CEnumerationPtr(nodemap.GetNode("ChunkSelector"))
    node_chunk_timestamp = node_chunk_selector.GetEntryByName("ImageTimestamp")
    if PySpin.IsReadable(node_chunk_timestamp):
        node_chunk_selector.SetIntValue(node_chunk_timestamp.GetValue())
    
    # 3. Enable the Timestamp Chunk
    node_chunk_enable = PySpin.CBooleanPtr(nodemap.GetNode("ChunkEnable"))
    if PySpin.IsWritable(node_chunk_enable):
        node_chunk_enable.SetValue(True)

def extract_timestamp(image):
    """Extracts the latched timestamp from the image chunk data in nanoseconds."""
    if image.HasChunkData():
        chunk_data = image.GetChunkData()
        timestamp = chunk_data.GetTimestamp()
        return timestamp  # Time in nanoseconds
    return None

# --- Typical Usage ---
# Assuming 'cam' is an initialized camera object
# cam.BeginAcquisition()
# image = cam.GetNextImage()
# timestamp_ns = extract_timestamp(image)
# print(f"Image captured at: {timestamp_ns} ns")
