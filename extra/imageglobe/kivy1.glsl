---VERTEX SHADER-------------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

/* Outputs to the fragment shader */
varying vec4 frag_color;
varying vec2 tex_coord1;

/* vertex attributes */
attribute vec3     v_pos;
attribute vec2     v_tc0;

/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;
uniform float      opacity;

void main (void) {
  frag_color = color * vec4(1.0, 1.0, 1.0, opacity);
  tex_coord1 = v_tc0;
//  gl_Position = projection_mat * modelview_mat * vec4(v_pos.xy, 0.0, 1.0);
  vec4 pos = modelview_mat * vec4(v_pos,1.0);
  gl_Position = projection_mat * pos;
}


---FRAGMENT SHADER-----------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord1;

/* uniform texture samplers */
uniform sampler2D texture1;

void main (void){
    gl_FragColor = frag_color * texture2D(texture1, tex_coord1);
}
