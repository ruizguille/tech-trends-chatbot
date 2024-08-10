import { EventSourceParserStream } from 'eventsource-parser/stream';

export async function* parseSSEStream(stream) {
  const reader = stream
    .pipeThrough(new TextDecoderStream())
    .pipeThrough(new EventSourceParserStream())
    .getReader();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    if (value.type === 'event') {
      yield value.data;
    }
  }
}
