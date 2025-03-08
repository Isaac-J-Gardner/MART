import moderngl
import numpy as np
from PIL import Image
import pygame

# Initialize ModernGL context
ctx = moderngl.create_standalone_context()

# Define the compute shader source code
compute_shader_source = '''
#version 430
layout(local_size_x=16, local_size_y=16) in;
layout(rgba8, binding=0) uniform image2D output_image;

uniform vec2 z;
uniform float scale_factor;

// Complex number operations
vec2 complex_add(vec2 a, vec2 b) {
    return a + b;
}

vec2 complex_mul(vec2 a, vec2 b) {
    return vec2(
        a.x * b.x - a.y * b.y,  // Real part
        a.x * b.y + a.y * b.x   // Imaginary part
    );
}

vec2 complex_sin(vec2 a) {
    return vec2(
        sin(a.x) * cosh(a.y),  // Real part
        cos(a.x) * sinh(a.y)   // Imaginary part
    );
}

float complex_abs(vec2 a) {
    return sqrt(a.x * a.x + a.y * a.y);
}

void main() {
    ivec2 pixel_coords = ivec2(gl_GlobalInvocationID.xy);
    vec2 c = vec2(
        float(pixel_coords.x - 256) / (32.0 * scale_factor),  // Map coordinates to complex plane
        float(pixel_coords.y - 256) / (32.0 * scale_factor)
    );
    
    int max_iterations = 100;
    int iteration = 0;

    for (int i = 0; i < max_iterations; i++) {
        c = complex_mul(complex_sin(c), c);
        if (complex_abs(c) > 50.0) {
            break;
        }
        iteration++;
    }

    // Map iteration count to a color
    float color = float(iteration) / float(max_iterations);
    imageStore(output_image, pixel_coords, vec4(color, color, color, 1.0));
}
'''

# Create a compute shader
compute_shader = ctx.compute_shader(compute_shader_source)

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0,0,0))
pygame.display.set_caption("Fractal Generator")
rect = pygame.Rect((50, 50), (512, 512))

clock = pygame.time.Clock()

Z = (0.0, 0.0)

scale_factor = 1.0

changing = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            if changing:
                mx, my = pygame.mouse.get_pos()
                if rect.collidepoint((mx, my)):
                    Z = ((mx - 306)/256, (-my + 306)/256)
        elif event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_l]:
                if changing == True:
                    changing = False
                else:
                    changing = True
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                scale_factor /= 1.1
            elif event.y < 0:
                scale_factor *= 1.1
            
                    

    compute_shader['z'] = Z
    compute_shader['scale_factor'] = scale_factor

    # Create a texture to store the output (512x512 RGBA8)
    texture = ctx.texture((512, 512), 4)
    texture.bind_to_image(0, read=False, write=True)

    # Run the compute shader
    compute_shader.run(group_x=32, group_y=32)  # 512 / 16 = 32 workgroups in X and Y

    # Read the texture data back to the CPU
    data = texture.read()
    image = np.frombuffer(data, dtype=np.uint8).reshape((512, 512, 4))
    
    image_pil = Image.fromarray(image, 'RGBA')
    mode = image_pil.mode
    size = image_pil.size
    data = image.tobytes()

    pyimage = pygame.image.fromstring(data, size, mode).convert()
    
    screen.fill((255,255,255))
    
    screen.blit(pyimage, (50, 30))

    pygame.display.flip()

    clock.tick(50)

# Quit pygame window
image_pil.save('fractal_output.png')

pygame.quit()	 
