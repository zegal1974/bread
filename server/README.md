

https://dnschecker.org/


```python
import ffmpeg  
  
input_file = 'path/to/your/media/file.mp4'  
output_file = 'path/to/your/output/file.txt'  
  
ffprobe_cmd = ffmpeg.input(input_file).output(output_file, f='ffprobe', format='null').run_async()  
ffprobe_out, _ = ffprobe_cmd.communicate()  
  
with open(output_file, 'r') as file:  
    probe_info = file.read()  
  
print(probe_info)
```

### TODO

1. clear magnet