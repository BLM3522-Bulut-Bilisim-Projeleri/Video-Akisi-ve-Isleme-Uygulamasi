from google.cloud import videointelligence_v1 as vi

def analyze_objects(video_path):
    client = vi.VideoIntelligenceServiceClient()

    with open(video_path, "rb") as file:
        input_content = file.read()

    features = [vi.Feature.OBJECT_TRACKING]

    operation = client.annotate_video(
        request={"features": features, "input_content": input_content}
    )

    result = operation.result(timeout=300)
    annotation_results = result.annotation_results[0]

    objects = []
    for obj in annotation_results.object_annotations:
        entity = obj.entity.description
        confidence = obj.confidence
        time_segment = obj.segment
        box = obj.frames[0].normalized_bounding_box  

        objects.append({
            "label": entity,
            "confidence": round(confidence, 2),
            "start_time": round(time_segment.start_time_offset.total_seconds(), 2),
            "end_time": round(time_segment.end_time_offset.total_seconds(), 2),
            "bounding_box": {
                "left": round(box.left, 2),
                "top": round(box.top, 2),
                "right": round(box.right, 2),
                "bottom": round(box.bottom, 2)
            }
        })

    return objects

