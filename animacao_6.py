# ANIMAÇÃO 6: 	Discussão sobre ângulo sólido
from manim import *
import numpy as np
from math import degrees
import math

class angulo_solido(ThreeDScene):
    def construct(self):
        # ================== ÂNGULO PLANO 2D ==================
        # Configura a câmera para visão de cima (plano XY)
        self.set_camera_orientation(phi=0, theta=-90*DEGREES)
        
        # ================== COMPONENTES DO ÂNGULO PLANO ==================
        # Cria os elementos do ângulo plano: centro, círculo e raios
        center = Dot(color=YELLOW)
        circle = Circle(radius=2, color=BLUE)
        circle.set_opacity(0.1)
        
        # Raios que definem o ângulo (30° e 60°)
        rays = VGroup(*[
            Line(ORIGIN, 2 * np.array([np.cos(angle), np.sin(angle), 0]), 
                color=YELLOW)
            for angle in [30*DEGREES, 60*DEGREES]
        ])
        
        # Arco que representa o ângulo (30°)
        arc = Arc(radius=1, angle=30*DEGREES, 
                start_angle=30*DEGREES, color=RED)
        arc.set_fill_color(RED)
        arc.set_opacity(0.5)
        
        # Rótulo do ângulo (θ)
        angle_label = MathTex(r"\theta", color=RED).scale(0.8).next_to(arc, UP)
        
        # ================== ANIMAÇÃO INICIAL (2D) ==================
        # Mostra o centro e o círculo (os raios e arco estão comentados)
        self.play(LaggedStart(Create(center), Create(circle)))  # , Create(rays)))
        # self.play(Create(arc))  # Arco não é mostrado nesta versão
        self.wait()

        # ================== TRANSIÇÃO PARA 3D ==================     
        # Move a câmera para uma vista 3D
        self.move_camera(phi=60*DEGREES, theta=25*DEGREES, zoom=0.8, run_time=2)
        
        # ================== ÂNGULO SÓLIDO 3D ==================
        # Função para criar um patch esférico retangular
        def create_spherical_patch(r, theta_range, phi_range):
            """Cria um retalho esférico retangular com vértices radiais"""
            return Surface(
                lambda u, v: r * np.array([
                    np.sin(v) * np.cos(u),  # x
                    np.sin(v) * np.sin(u),  # y
                    np.cos(v)               # z
                ]),
                u_range=phi_range,    # Intervalo do ângulo azimutal
                v_range=theta_range,  # Intervalo do ângulo polar
                resolution=(5, 5),    # Resolução baixa para ver os quadrados
                color=GREEN
            ).set_opacity(0.4).set_color('#00FFFF')  # Cor ciano

        # Define dois raios para esferas concêntricas
        r1, r2 = 2.0, 3.0
        
        # Cria duas esferas concêntricas com diferentes raios e opacidades
        sphere1 = Sphere(radius=r1, resolution=(20,20)).set_opacity(0.3)
        sphere2 = Sphere(radius=r2, resolution=(20,20)).set_opacity(0.2)
        
        # Dimensões angulares para os patches (mesmo para ambas as esferas)
        theta_min, theta_max = PI/6, PI/3   # Ângulo polar: 30° a 60°
        phi_min, phi_max = PI/4, PI/2       # Ângulo azimutal: 45° a 90°
        
        # Cria patches (retalhos) nas duas esferas
        patch1 = create_spherical_patch(r1, [theta_min, theta_max], [phi_min, phi_max])
        patch2 = create_spherical_patch(r2, [theta_min, theta_max], [phi_min, phi_max])

        # Função para calcular os vértices radiais de um patch
        def get_radial_vertices(r, theta_range, phi_range):
            """Calcula os vértices radiais de um patch esférico"""
            return [
                r * np.array([
                    np.sin(theta) * np.cos(phi),
                    np.sin(theta) * np.sin(phi),
                    np.cos(theta)
                ])
                for theta in [theta_range[0], theta_range[1]]
                for phi in [phi_range[0], phi_range[1]]
            ]

        # Cria linhas radiais conectando a origem aos vértices dos patches
        lines1 = VGroup(*[
            Line(ORIGIN, vertex, color=BLUE_B, stroke_width=1.5)
            for vertex in get_radial_vertices(r1, [theta_min, theta_max], [phi_min, phi_max])
        ])
        
        lines2 = VGroup(*[
            Line(ORIGIN, vertex, color=RED_B, stroke_width=1.5)
            for vertex in get_radial_vertices(r2, [theta_min, theta_max], [phi_min, phi_max])
        ])
        
        # ================== ANIMAÇÃO DAS ESFERAS E PATCHES ==================
        # Anima a primeira esfera, seu patch e linhas radiais
        self.play(
            LaggedStart(
                Create(sphere1),
                Create(patch1),
                lag_ratio=0.5
            ), LaggedStart(*[Create(l) for l in lines1], lag_ratio=0.1),
            run_time=4
        )
        
        # Remove alguns elementos 2D (comentados)
        # self.play(FadeOut(rays, angle_label))
        # self.play(FadeOut(arc))
        self.wait()
        
        # Zoom e criação da segunda esfera com seu patch e linhas
        self.move_camera(zoom=1, run_time=2)
        self.play(
            Create(sphere2),
            Create(patch2), 
            LaggedStart(*[Create(l) for l in lines2], lag_ratio=0.1),
            run_time=4
        )
        
        # ================== EQUAÇÃO DO ÂNGULO SÓLIDO ==================
        # Adiciona a equação que define o ângulo sólido (fixa na tela)
        equation = MathTex(
            r"\Omega = \frac{A}{r^2} = \text{constante}",
            font_size=36
        ).to_edge(UR)
        
        # Atualizador para manter a equação fixa no quadro durante movimentos da câmera
        equation.add_updater(lambda v: self.add_fixed_in_frame_mobjects(v))
        
        # Símbolo do ângulo sólido próximo ao centro
        omega_angle = MathTex(r"\Omega").next_to(center)
        
        # Adiciona ambos à cena como objetos fixos no quadro
        self.add_fixed_in_frame_mobjects(equation)
        self.add_fixed_in_frame_mobjects(omega_angle)
        
        # Ajusta a câmera para focar na segunda esfera
        self.move_camera(zoom=0.7, focal_point=sphere2.get_center(), run_time=3)
        
        # Inicia rotação suave da câmera para visualização 3D
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(5)

        # ================== TRANSFORMAÇÕES VISUAIS ==================
        # Remove as esferas e o círculo, depois os traz de volta
        self.play(FadeOut(sphere2, sphere1, circle))
        self.wait(7)
        self.stop_ambient_camera_rotation()
        self.wait()
        self.play(FadeIn(sphere1, sphere2, circle))
        self.wait(2)

        # ================== VETORES NORMAIS ==================
        # Calcula os centros dos patches e as normais radiais unitárias
        patch_center1 = np.array(patch1.get_center(), dtype=float)
        radial_normal1 = patch_center1 / np.linalg.norm(patch_center1)
        
        patch_center2 = np.array(patch2.get_center(), dtype=float)
        radial_normal2 = patch_center2 / np.linalg.norm(patch_center2)
        
        # Cria o vetor normal para o patch interno
        normal_vector_1 = Arrow3D(
            start=patch_center1,
            end=patch_center1 + radial_normal1,
            color=WHITE
        )
        normal_vector_label_1 = MathTex(
            r"\hat{\mathbf{n}}", 
            font_size=10
        ).next_to(normal_vector_1)
        normal_vector_label_1.add_updater(lambda v: self.add_fixed_in_frame_mobjects(v))
        
        # Cria o vetor normal para o patch externo (com z-index alto)
        normal_vector_2 = Arrow3D(
            start=patch_center2,
            end=patch_center2 + radial_normal2,
            color=WHITE
        ).set_z_index(+5)
        normal_vector_label_2 = MathTex(
            r"\hat{\mathbf{n}}", 
            font_size=10
        ).next_to(normal_vector_2)
        normal_vector_label_2.add_updater(lambda v: self.add_fixed_in_frame_mobjects(v))
        
        # ================== ANIMAÇÃO DOS VETORES NORMAIS ==================
        # Muda a cor da primeira esfera para vermelho
        self.play(sphere1.animate.set_stroke(color=RED, width=0.5))
        self.wait(2)
        
        # Remove o patch externo e suas linhas
        self.play(FadeOut(patch2, lines2))
        self.wait(5)
        
        # Mostra o vetor normal interno
        self.play(FadeIn(normal_vector_1))
        self.wait(5)
        
        # Remove o vetor normal interno
        self.remove(normal_vector_1)
        self.wait(2)
        
        # Traz de volta o patch externo, linhas e mostra o vetor normal externo
        self.play(FadeIn(patch2, lines2, normal_vector_2))
        self.wait(5)
        
        # Zoom no vetor normal externo
        self.move_camera(zoom=2, focal_point=normal_vector_2.get_center(), run_time=3)

        self.wait(2)
