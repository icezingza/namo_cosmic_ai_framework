# API Reference

## POST /memory
Create a new memory with optional emotional context.

### Request Body
- `content` (string): Memory content.
- `emotional_context` (object, optional): Emotion intensity mapping.

### Response
Returns metadata about the created memory including reliability score and cosmic signature.

## GET /memory
Recall memories that match the supplied query.

### Query Parameters
- `query` (string): Text to search within memories.

### Response
A list of memories with associated metadata.

## GET /system/health
Health status of the Infinity AI deployment including internal metrics.
