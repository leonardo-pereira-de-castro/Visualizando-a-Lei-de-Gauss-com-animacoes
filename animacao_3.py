# Fluxo do campo elétrico gerado por uma partícula carregada em uma superfície esférica
from manim import *
from manim_physics import *
import numpy as np
from math import degrees
import math

class campo_E_3D(ThreeDScene):
    def construct(self):
        # ============================================================
        # 1. FUNÇÃO AUXILIAR: CRIAÇÃO DE PATCH ESFÉRICO
        # ============================================================
        
        def create_spherical_patch(r, theta_range, phi_range):
            """
            Cria um retalho (patch) retangular sobre uma superfície esférica.
            
            Parâmetros:
            r: raio da esfera
            theta_range: intervalo do ângulo polar (co-latitude) em radianos
            phi_range: intervalo do ângulo azimutal (longitude) em radianos
            
            Retorna:
            Uma superfície paramétrica representando o patch esférico
            """
            return Surface(
                lambda u, v: r * np.array([
                    np.sin(v) * np.cos(u),  # Coordenada x
                    np.sin(v) * np.sin(u),  # Coordenada y
                    np.cos(v)               # Coordenada z
                ]),
                u_range=phi_range,    # Intervalo do ângulo azimutal
                v_range=theta_range,  # Intervalo do ângulo polar
                resolution=(10, 10),  # Resolução da malha (u_res, v_res)
                color=GREEN           # Cor base do patch
            ).set_opacity(0.4)        # Transparência para visualização interna
        
        # ============================================================
        # 2. DEFINIÇÃO DAS ESFERAS CONCÊNTRICAS (SUPERFÍCIES GAUSSIANAS)
        # ============================================================
        
        # Definindo os raios das esferas concêntricas
        # Cada esfera representa uma superfície gaussiana com diferente raio
        r1, r2, r3, r4 = 1.5, 3.5, 2.5, 0.75
        
        # Criação das esferas com diferentes propriedades visuais
        # Todas são centradas na origem e têm baixa opacidade para visualização interna
        sphere1 = Sphere(radius=r1, resolution=(30,30), stroke_width=0.4).set_opacity(0.1).set_fill_color(RED_A)
        sphere2 = Sphere(radius=r2, resolution=(30,30), stroke_width=0.1).set_opacity(0.1).set_fill_color(RED_A)
        sphere3 = Sphere(radius=r3, resolution=(30,30), stroke_width=0.4).set_opacity(0.1).set_fill_color(RED_A)
        sphere4 = Sphere(radius=r4, resolution=(30,30), stroke_width=0.4).set_opacity(0.1).set_fill_color(RED_A)
        
        # ============================================================
        # 3. CRIAÇÃO DAS LINHAS DE CAMPO ELÉTRICO RADIAIS
        # ============================================================
        
        # Definição dos ângulos para distribuição uniforme das linhas de campo
        theta_range = np.linspace(0, PI, 8)      # Ângulo polar: 0 a π (norte a sul)
        phi_range = np.linspace(0, 2*PI, 16)     # Ângulo azimutal: 0 a 2π (volta completa)
        
        # Grupo para armazenar as linhas de campo da esfera maior (raio 3.5)
        field_lines = VGroup()
        
        # Criação das linhas de campo radiais (excluindo polos para evitar sobreposição)
        for theta in theta_range[1:-1]:          # Exclui θ=0 e θ=π (polos)
            for phi in phi_range[1:-1]:          # Exclui φ=0 e φ=2π (para evitar duplicação)
                # Converte coordenadas esféricas para cartesianas
                x = 3.5 * np.sin(theta) * np.cos(phi)
                y = 3.5 * np.sin(theta) * np.sin(phi)
                z = 3.5 * np.cos(theta)
                patch_center = np.array([x, y, z])
                
                # Calcula vetor normal radial (unitário, apontando para fora)
                radial_normal = patch_center / np.linalg.norm(patch_center)
                
                # Cria seta 3D representando linha de campo
                field_line = Arrow3D(
                    start=ORIGIN,                     # Origem no centro da carga
                    end=patch_center + 1.5*radial_normal,  # Direção radial para fora
                    thickness=0.01,                   # Espessura fina para visualização clara
                    color=RED,                        # Vermelho para campo elétrico
                    resolution=8                      # Resolução da seta 3D
                )
                field_lines.add(field_line)
        
        # Criação das linhas de campo nos polos (tratamento especial)
        for theta in [0, 2*PI]:
            patch_center = np.array([0, 0, 3*np.cos(theta)])
            radial_normal = np.array([0, 0, np.cos(theta)])
            field_line = Arrow3D(
                start=ORIGIN,
                end=patch_center + 1.5*radial_normal,
                thickness=0.01,
                color=RED,
            )
            field_lines.add(field_line)
            
        # Configuração visual comum a todas as linhas de campo
        field_lines.set_opacity(0.15).set_z_index(-2)  # Baixa opacidade e fundo
        
        # ============================================================
        # 4. LINHAS DE CAMPO PARA AS OUTRAS ESFERAS CONCÊNTRICAS
        # ============================================================
        # Nota: O código é repetido para cada raio diferente, mostrando que o
        # padrão radial é o mesmo independentemente do raio da superfície gaussiana
        
        # Linhas de campo para esfera com raio 2.5
        field_lines_2 = VGroup()
        for theta in theta_range[1:-1]:
            for phi in phi_range[1:-1]:
                x = 2.5 * np.sin(theta) * np.cos(phi)
                y = 2.5 * np.sin(theta) * np.sin(phi)
                z = 2.5 * np.cos(theta)
                patch_center_2 = np.array([x, y, z])
                radial_normal_2 = patch_center_2 / np.linalg.norm(patch_center_2)
                field_line_2 = Arrow3D(
                    start=ORIGIN,
                    end=patch_center_2 + 1.5*radial_normal_2,
                    thickness=0.01,
                    color=RED,
                    resolution=8
                )
                field_lines_2.add(field_line_2)
        
        # Polos para esfera com raio 2.5
        for theta in [0, PI]:
            patch_center_2 = np.array([0, 0, 3*np.cos(theta)])
            radial_normal_2 = np.array([0, 0, np.cos(theta)])
            field_line_2 = Arrow3D(
                start=ORIGIN,
                end=patch_center_2 + 1.5*radial_normal_2,
                thickness=0.01,
                color=RED,
            )
            field_lines_2.add(field_line_2)
        field_lines_2.set_opacity(0.15).set_z_index(-2)
        
        # Linhas de campo para esfera com raio 1.5
        field_lines_3 = VGroup()
        for theta in theta_range[1:-1]:
            for phi in phi_range[1:-1]:
                x = 1.5 * np.sin(theta) * np.cos(phi)
                y = 1.5 * np.sin(theta) * np.sin(phi)
                z = 1.5 * np.cos(theta)
                patch_center_3 = np.array([x, y, z])
                radial_normal_3 = patch_center_3 / np.linalg.norm(patch_center_3)
                field_line_3 = Arrow3D(
                    start=ORIGIN,
                    end=patch_center_3 + 1.5*radial_normal_3,
                    thickness=0.01,
                    color=RED,
                    resolution=8
                )
                field_lines_3.add(field_line_3)
        
        # Polos para esfera com raio 1.5
        for theta in [0, PI]:
            patch_center_3 = np.array([0, 0, 3*np.cos(theta)])
            radial_normal_3 = np.array([0, 0, np.cos(theta)])
            field_line_3 = Arrow3D(
                start=ORIGIN,
                end=patch_center_3 + 1.5*radial_normal_3,
                thickness=0.01,
                color=RED,
            )
            field_lines_3.add(field_line_3)
        field_lines_3.set_opacity(0.15).set_z_index(-2)
        
        # Linhas de campo para esfera com raio 0.75
        field_lines_4 = VGroup()
        for theta in theta_range[1:-1]:
            for phi in phi_range[1:-1]:
                x = 0.75 * np.sin(theta) * np.cos(phi)
                y = 0.75 * np.sin(theta) * np.sin(phi)
                z = 0.75 * np.cos(theta)
                patch_center_4 = np.array([x, y, z])
                radial_normal_4 = patch_center_4 / np.linalg.norm(patch_center_4)
                field_line_4 = Arrow3D(
                    start=ORIGIN,
                    end=patch_center_4 + 1.5*radial_normal_4,
                    thickness=0.01,
                    color=RED,
                    resolution=8
                )
                field_lines_4.add(field_line_4)
        
        # Polos para esfera com raio 0.75
        for theta in [0, PI]:
            patch_center_4 = np.array([0, 0, 3*np.cos(theta)])
            radial_normal_4 = np.array([0, 0, np.cos(theta)])
            field_line_4 = Arrow3D(
                start=ORIGIN,
                end=patch_center_4 + 1.5*radial_normal_4,
                thickness=0.01,
                color=RED,
            )
            field_lines_4.add(field_line_4)
        field_lines_4.set_opacity(0.15).set_z_index(-2)
        
        # ============================================================
        # 5. DEFINIÇÃO DOS PATCHES ESFÉRICOS (ELEMENTOS DE ÁREA)
        # ============================================================
        
        # Ângulos que definem o patch (retalho) esférico
        theta_min, theta_max = PI/6, PI/3   # Intervalo do ângulo polar
        phi_min, phi_max = PI/4, PI/2       # Intervalo do ângulo azimutal
        
        # Criação dos patches nas duas esferas concêntricas
        patch1 = create_spherical_patch(r1, [theta_min, theta_max], [phi_min, phi_max]).set_fill_color(RED_C)
        patch2 = create_spherical_patch(r2, [theta_min, theta_max], [phi_min, phi_max]).set_color(PURPLE_C)
   
        # Função para calcular vértices radiais de um patch
        def get_radial_vertices(r, theta_range, phi_range):
            """
            Calcula as coordenadas cartesianas dos 4 vértices de um patch esférico.
            
            Retorna:
            Lista de 4 pontos 3D nos vértices do patch
            """
            return [
                r * np.array([
                    np.sin(theta) * np.cos(phi),
                    np.sin(theta) * np.sin(phi),
                    np.cos(theta)
                ])
                for theta in [theta_range[0], theta_range[1]]  # Dois valores de θ
                for phi in [phi_range[0], phi_range[1]]        # Dois valores de φ
            ]
        
        # ============================================================
        # 6. ELEMENTOS CENTRAIS: CARGAS E PONTO DE REFERÊNCIA
        # ============================================================
        
        # Centro do sistema (origem)
        center = Dot(color=YELLOW).set_opacity(0)
        
        # Carga positiva (vermelha)
        charge_pos = Charge(magnitude=+3, color=RED).set_opacity(0)
        circle_charge = Sphere(radius=0.4, color=RED, resolution=(30,30), stroke_width=0.01).set_opacity(0.9).set_fill_color(RED)
        circle = VGroup(center, circle_charge).set_z_index(+2)  # Frente de outros objetos
        
        # Carga negativa (azul)
        charge_neg = Charge(magnitude=-3, color=BLUE)
        circle_charge_neg = Sphere(radius=0.4, color=BLUE, resolution=(30,30), stroke_width=0.01).set_opacity(0.9).set_fill_color(BLUE)
        circle_neg = VGroup(circle_charge_neg).set_z_index(+2)

        # ============================================================
        # 7. PONTO P NA SUPERFÍCIE E LINHA RADIAL r
        # ============================================================
        
        # Calcula o centro do patch2 (ponto P na superfície esférica)
        patch_center_p = np.array(patch2.get_center(), dtype=float)
        radial_normal = patch_center_p / np.linalg.norm(patch_center_p)  # Normal unitária em P

        # Elementos visuais para o ponto P
        P_point = Dot3D(point=patch_center_p, color=YELLOW, radius=0.04).set_z_index(+5)
        line_P = Line(start=ORIGIN, end=P_point, color=WHITE, stroke_width=1.5).set_opacity(0.5)
        label_P = Tex("P", font_size=25).next_to(P_point, buff=0.2)
        label_R = Tex("r", font_size=25).next_to(line_P, buff=0.5)

        # ============================================================
        # 8. LINHAS RADIAIS DE CONEXÃO E VETORES DE CAMPO
        # ============================================================
        
        # Linhas do centro até os vértices do patch interno (raio r1)
        lines1 = VGroup(*[
            Line(ORIGIN, vertex, color=RED_A, stroke_width=1.0)
            for vertex in get_radial_vertices(r1, [theta_min, theta_max], [phi_min, phi_max])
        ]).set_opacity(0.5)
        
        # Linhas do centro até os vértices do patch externo (raio r2)
        lines2 = VGroup(*[
            Line(ORIGIN, vertex, color=GOLD_A, stroke_width=1.0)
            for vertex in get_radial_vertices(r2, [theta_min, theta_max], [phi_min, phi_max])
        ]).set_opacity(0.5)

        # Vetor de campo elétrico no ponto P (para carga positiva)
        field_line = Arrow3D(start=ORIGIN, end=patch_center_p + 1.5*radial_normal,
                            thickness=0.01, color=RED)
        
        # Vetor de campo elétrico no ponto P (para carga negativa)
        field_line_neg = Arrow3D(start=patch_center_p, end=patch_center_p - radial_normal,
                                thickness=0.01, color=BLUE)
        
        # ============================================================
        # 9. VETORES NORMAIS À SUPERFÍCIE
        # ============================================================
        
        # Vetor normal curto (para destaque visual)
        normal_vector_2 = Arrow3D(start=patch_center_p,
                                end=patch_center_p + radial_normal/3,
                                color=PURPLE_A,
                                thickness=0.01).set_z_index(-1)

        # Vetor normal completo (representa n̂)
        normal_vector_1 = Arrow3D(start=patch_center_p,
                                end=patch_center_p + radial_normal,
                                color=WHITE,
                                thickness=0.01).set_z_index(+1)

        # ============================================================
        # 10. SEQUÊNCIA PRINCIPAL DE ANIMAÇÕES
        # ============================================================
        
        # Configuração inicial da câmera 3D
        self.set_camera_orientation(phi=60*DEGREES, theta=25*DEGREES, zoom=1.2, run_time=2)
        
        # A. Introdução da carga positiva no centro
        self.play(LaggedStart(Create(center), FadeIn(center, circle_charge, circle),
                              lag_ratio=3))
        self.wait()
        self.wait(5)

        # B. Apresentação da superfície gaussiana esférica (raio maior)
        self.play(Create(sphere2))
        self.wait(4)
                  
        # C. Destaque do patch e linhas radiais na superfície
        self.play(Create(patch2),
              LaggedStart(*[Create(l) for l in lines2], lag_ratio=0.1),
              run_time=5)
        self.wait(4)

        # D. Ajuste da câmera para melhor visualização
        self.move_camera(phi=55*DEGREES, theta=0*DEGREES, zoom=0.8, run_time=2)
        self.wait(3)
    
        # E. Introdução do vetor normal à superfície
        self.play(FadeIn(normal_vector_1), run_time=2)
        
        # F. Remoção da esfera para visualização mais clara
        self.play(FadeOut(sphere2))
        self.wait(3)

        # G. Introdução do vetor de campo elétrico (carga positiva)
        self.play(FadeIn(field_line))   
        self.wait(4)
        
        # H. Zoom no patch para análise detalhada
        self.move_camera(frame_center=(patch2),
                         default_frame_stroke_color=ManimColor('#FFFFFF'),
                         default_frame_stroke_width=0,
                         zoom=1.8, run_time=3)
        self.wait(5)
        
        # I. Transição para carga negativa (mostra diferença de direção)
        self.play(LaggedStart(FadeOut(circle_charge, field_line),
                              FadeIn(circle_charge_neg, field_line_neg),
                              lag_ratio=2))
        self.wait(3)
        
        # J. Retorno à visão geral
        self.move_camera(frame_center=(ORIGIN),
                         default_frame_stroke_color=ManimColor('#FFFFFF'),
                         default_frame_stroke_width=0,
                         zoom=1.0, run_time=3)
        self.wait(3)
        
        # K. Retorno à carga positiva
        self.play(LaggedStart(FadeOut(circle_charge_neg, field_line_neg),
                              FadeIn(circle_charge, field_line),
                              lag_ratio=2))
        self.wait(3)
        
        # L. Limpeza dos elementos detalhados e retorno à esfera
        self.play(FadeOut(lines2, patch2, field_line, normal_vector_1, P_point))
        self.play(FadeIn(sphere2))
        self.wait(3)
        
        # M. Apresentação de todas as linhas de campo radiais
        self.play(FadeIn(field_lines))  
        self.wait(5)
        
        # N. Início da rotação suave da câmera para visualização 3D
        self.begin_ambient_camera_rotation()
        self.wait(3)
        
        # O. Sequência de transição entre diferentes superfícies gaussianas
        # Mostra que o padrão de linhas de campo é o mesmo para diferentes raios
        self.play(FadeOut(field_line))
        self.play(FadeOut(sphere2))
        self.play(FadeIn(sphere3, field_lines_2))
        self.wait(3)
        
        self.play(FadeOut(field_line_2, sphere3))
        self.play(FadeIn(sphere1, field_lines_3))
        self.wait(3)
        
        self.play(FadeOut(field_line_3, sphere1))
        self.play(FadeIn(sphere4, field_lines_4))
        self.wait(4)
        
        # P. Finalização: remoção gradual dos elementos
        self.play(FadeOut(sphere4), run_time=5)
        self.wait(5)