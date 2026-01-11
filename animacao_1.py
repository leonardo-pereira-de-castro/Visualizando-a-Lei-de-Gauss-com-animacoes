# ANIMAÇÃO 1: Fluxo do campo elétrico através de uma superfície plana
from manim import *
import numpy as np
from math import degrees
import math

class open_flux(ThreeDScene):
    def construct(self):
        # ============================================================
        # 1. CONFIGURAÇÃO INICIAL DA CENA E CONTROLES INTERATIVOS
        # ============================================================
        
        # Define a orientação inicial da câmera no espaço 3D (ângulos phi, theta, zoom e rotação gamma)
        self.set_camera_orientation(phi=60*DEGREES, theta=55*DEGREES, zoom=1.5, gamma=0)
        
        # Rastreador para controlar o fator de escala (tamanho) da superfície
        scale_factor_tracker = ValueTracker(1)
        
        # Rastreador para controlar o ângulo de rotação da superfície (inicia em 90 graus = PI/2 rad)
        angle_tracker = ValueTracker(PI/2)
        
        # Display numérico que mostra o ângulo atual em graus. Atualiza automaticamente.
        angle_display = DecimalNumber(
            np.degrees(angle_tracker.get_value()),  # Valor inicial convertido para graus
            num_decimal_places=1,                   # Uma casa decimal
            include_sign=False,                     # Não mostra sinal de positivo/negativo
            color=WHITE,                            # Cor do texto
            unit=r"^\circ"                          # Símbolo de graus
        ).add_updater(
            lambda d: d.set_value(np.degrees(angle_tracker.get_value()))  # Atualiza o valor em graus
        ).to_corner(3 * DR).add_updater(  # Posiciona no canto inferior direito
            lambda v: self.add_fixed_in_frame_mobjects(v)  # Mantém o objeto fixo na tela (não gira com a cena 3D)
        )

        # ============================================================
        # 2. CONSTRUÇÃO DO INDICADOR VISUAL DO ÂNGULO (linhas e arco)
        # ============================================================
        
        # Linha de referência fixa (horizontal, eixo X positivo)
        line_initial = Line(ORIGIN, RIGHT*0.5, color=WHITE)
        
        # Linha que rotaciona de acordo com o ângulo. É redesenhada continuamente.
        line_rotating = always_redraw(lambda: Line(
            ORIGIN,
            [0.5*np.cos(angle_tracker.get_value()),
             0,
             0.5*np.sin(angle_tracker.get_value())],
            color=WHITE
        ))
        
        # Arco amarelo que ilustra o ângulo entre as duas linhas
        arc_angle = always_redraw(lambda: ParametricFunction(
            lambda t: np.array([
                0.5*np.cos(t),
                0,
                0.5*np.sin(t)
            ]),
            t_range=[0, angle_tracker.get_value()],  # O arco se estende do eixo X até a linha rotacionada
            color=YELLOW
        ))

        # Rótulo do ângulo (símbolo theta). Fixo no canto superior esquerdo.
        theta_arc_label = MathTex(r"\theta").move_to(UL*2.5).add_updater(lambda v: self.add_fixed_in_frame_mobjects(v))
        theta_arc_label.set_color(YELLOW)

        # Agrupa os elementos visuais do ângulo para facilitar o gerenciamento
        angle_group = VGroup(line_initial, line_rotating, arc_angle)
        angle_group.set_z_index(10)  # Garante que fique acima de outros objetos

        # ============================================================
        # 3. DEFINIÇÃO DA SUPERFÍCIE PLANA (PRISMA FINO)
        # ============================================================
        
        # Cria um prisma fino (simulando uma superfície 2D no espaço 3D)
        sq = Prism(dimensions=[1.5, 2.0, 0.02]).move_to(ORIGIN)
        sq.set_fill(color='#00FFFF', opacity=0.3)  # Cor ciano com baixa opacidade
        sq.set_stroke(color=WHITE, width=0.5)      # Borda branca fina
        sq.rotate(angle_tracker.get_value())       # Rotação inicial definida pelo rastreador
        sq.set_z_index(+5)                         # Define a ordem de sobreposição

        # ============================================================
        # 4. DEFINIÇÃO DOS VETORES PRINCIPAIS
        # ============================================================
        
        # Vetor normal (n̂) à superfície. Atualiza sua direção conforme o ângulo muda.
        normal_arrow = always_redraw(lambda: Arrow3D(
            start=sq.get_center(),
            end=[1.0 * np.cos(angle_tracker.get_value()), 0, 1.0 * np.sin(angle_tracker.get_value())],
            color=PURE_BLUE,
            resolution=8  # Número de segmentos para suavizar a seta 3D
        ))
        normal_arrow.set_z_index(+10)
        normal_arrow.set_opacity(0.9)

        # ============================================================
        # 5. CÓPIA DA SUPERFÍCIE PARA ANIMAÇÃO DE ROTAÇÃO E ESCALA
        # ============================================================
        
        # Cria uma cópia da superfície que será usada para animações de rotação e escala.
        # É redesenhada continuamente para refletir mudanças no ângulo e no tamanho.
        rotating_prism = always_redraw(lambda: sq.copy().move_to(ORIGIN).rotate(
            angle_tracker.get_value() + PI/2,  # Rotação adicional de 90 graus
            axis=DOWN,                         # Eixo de rotação (para baixo)
            about_point=ORIGIN                 # Ponto de origem da rotação
        ).scale(scale_factor_tracker.get_value()))  # Aplica o fator de escala

        # Agrupa a superfície rotacionada com o vetor normal
        norma_plano = VGroup(rotating_prism, normal_arrow)

        # Vetor do campo elétrico (E). FIXO na direção do eixo X positivo.
        flux_arrow = Arrow3D(
            start=sq.get_center(),
            end=np.array([1.0, 0.0, 0.0]),
            color=RED,
        )
        flux_arrow.set_z_index(+6)

        # ============================================================
        # 6. DISPLAY NUMÉRICO PARA O FATOR DE ESCALA (ÁREA)
        # ============================================================
        
        # Mostra o valor atual do fator de escala (representando a área A)
        area_tracker = DecimalNumber(
            scale_factor_tracker.get_value(),
            num_decimal_places=1,
            include_sign=False,
            color=WHITE,
        ).to_corner(3 * DR).add_updater(
            lambda v: self.add_fixed_in_frame_mobjects(v)  # Mantém fixo na tela
        )

        # ============================================================
        # 7. EQUAÇÃO DO FLUXO (ATUALIZADA DINAMICAMENTE)
        # ============================================================
        
        # Versão inicial da equação, posicionada abaixo do mostrador de ângulo
        flux_equation = MathTex(
            r"\Phi =|\vec{E}| \cdot |\vec{A}| \cdot \cos(\theta)",
            substrings_to_isolate=[r"\cos(\theta)", r"|\vec{E}|", r"|\vec{A}|", r"\Phi"],
        ).next_to(angle_display, DOWN*2)

        # Versão fixa da equação, posicionada no canto superior direito (não atualiza)
        flux_equation_fixed = MathTex(
            r"\Phi =|\vec{E}|\cdot|\vec{A}|\cdot\cos(\theta)",
            substrings_to_isolate=[r"\cos(\theta)", r"|\vec{E}|", r"|\vec{A}|", r"\Phi"],
        ).to_corner(UR).set_color(YELLOW)

        # Atualizador que substitui a equação por uma versão com o valor numérico calculado
        flux_equation.add_updater(
            lambda m: m.become(
                MathTex(
                    r"\Phi = "  # Símbolo do fluxo
                    + f"{math.cos(angle_tracker.get_value()) * scale_factor_tracker.get_value():.2f}"  # Valor calculado: cos(θ) * A
                ).move_to(m.get_center())
            )
        ).add_updater(
            lambda v: self.add_fixed_in_frame_mobjects(v)  # Mantém fixo na tela
        )

        # Unidade do fluxo (N.m²/C)
        flux_unit = MathTex(r"N.m^2/C", font_size=25).add_updater(lambda v: self.add_fixed_in_frame_mobjects(v))
        flux_unit.move_to(flux_equation, RIGHT)

        # Rótulo "θ =" ao lado do mostrador numérico
        angle_label = MathTex(r"\theta =").next_to(angle_display, LEFT).add_updater(
            lambda v: self.add_fixed_in_frame_mobjects(v)
        )

        # ============================================================
        # 8. RÓTULOS E LEGENDAS PARA OS ELEMENTOS DA CENA
        # ============================================================
        
        n_tetha = MathTex(r"\theta", color=YELLOW).move_to(DL*4)
        n_hat = MathTex(r"\hat{n}", color=BLUE).next_to(normal_arrow, UL*4)
        n_area = MathTex(r"\vec{A} = A\hat{n}", color=BLUE).next_to(sq, RIGHT*6)
        campo_E = MathTex(r"\vec{E}", color=RED).move_to(LEFT*(5))

        # ============================================================
        # 9. CRIAÇÃO DO CAMPO VETORIAL (LINHAS DE CAMPO ELÉTRICO)
        # ============================================================
        
        # Função que cria um vetor individual do campo
        def create_vector(x, y, z):
            direction = np.array([2.0, 0.0, 0.0]) / 2  # Direção constante (eixo X)
            start_point = np.array([x, y, z])
            end_point = start_point + direction
            arrow = Arrow3D(
                start=start_point,
                end=end_point,
                color=RED,
                thickness=0.01,
                resolution=8,  # Suavidade da seta 3D
            )
            return arrow

        # Define intervalos para gerar uma grade 3D de vetores
        x_range = np.arange(-2.0, 2.0, 1.5)
        y_range = np.arange(-2.5, 1.25, 1.5)
        z_range = np.arange(-1.5, 1.5, 0.75)

        # Grupo que armazenará todos os vetores do campo
        vector_field = VGroup()

        # Cria manualmente os vetores em uma grade 3D
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    vector_field.add(create_vector(x, y, z))

        vector_field.z_index = -2  # Coloca os vetores atrás de outros objetos

        # Função para atualizar a visibilidade dos vetores (opacidade)
        def update_visibility(mobject):
            for arrow in vector_field:
                start = arrow.get_start()
                # Verifica se o vetor está dentro do volume do prisma
                if (-0.75 <= start[0] <= 0.75 and
                    -2.0 <= start[1] <= 2.0 and
                    -0.25 <= start[2] <= 0.25):
                    arrow.set_opacity(0.2)   # Mais transparente se estiver "atrás" da superfície
                else:
                    arrow.set_opacity(0.3)   # Mais visível se estiver "fora" da superfície

        # Conecta a função de atualização ao campo vetorial
        vector_field.add_updater(update_visibility)

        # ============================================================
        # 10. SEQUÊNCIA PRINCIPAL DE ANIMAÇÕES
        # ============================================================
        
        # --- INTRODUÇÃO DOS OBJETOS PRINCIPAIS ---
        self.play(FadeIn(norma_plano))
        self.wait()
        self.add_fixed_in_frame_mobjects(n_hat)
        self.play(Circumscribe(sq, fade_out=True, time_width=5))  # Destaque na superfície
        self.add_fixed_in_frame_mobjects(n_area)
        self.wait()

        # --- MUDANÇA DE VISTA DA CÂMERA ---
        self.move_camera(phi=90*DEGREES, theta=90*DEGREES, zoom=1.75, run_time=3.5)
        self.wait(2)

        # --- ADIÇÃO DOS DISPLAYS DE INFORMAÇÃO ---
        self.add_fixed_in_frame_mobjects(angle_label)
        self.add_fixed_in_frame_mobjects(angle_display)
        self.add_fixed_in_frame_mobjects(flux_equation)
        self.add_fixed_in_frame_mobjects(flux_equation_fixed)

        self.play(FadeOut(n_area, n_hat))
        self.wait()

        # --- INTRODUÇÃO DO CAMPO VETORIAL ---
        self.play(FadeIn(vector_field))
        self.add_fixed_in_frame_mobjects(campo_E)
        self.wait(3)
        self.play(FadeOut(campo_E))

        # --- ROTAÇÕES DA SUPERFÍCIE (VARIAÇÃO DE θ) ---
        self.play(angle_tracker.animate.set_value(PI/4), run_time=7, rate_func=smooth)
        self.wait(2)
        self.play(angle_tracker.animate.set_value(0), run_time=7, rate_func=smooth)
        self.wait(2)

        # --- MUDANÇA DE VISTA DA CÂMERA (NOVA PERSPECTIVA) ---
        self.move_camera(phi=60*DEGREES, theta=30*DEGREES, zoom=1.75, run_time=3.5)
        self.wait(2)

        # --- VARIAÇÃO DA ÁREA (FATOR DE ESCALA) ---
        self.play(scale_factor_tracker.animate.set_value(2), run_time=5, rate_functions=smooth)
        self.wait()
        self.play(scale_factor_tracker.animate.set_value(0.5), run_time=5, rate_functions=smooth)
        self.wait()
        self.play(scale_factor_tracker.animate.set_value(1), run_time=5, rate_functions=smooth)
        self.wait()

        # --- FINALIZAÇÃO DA PRIMEIRA PARTE ---
        self.play(FadeOut(vector_field))
        self.wait()

        # --- MUDANÇA DE VISTA DA CÂMERA ---
        self.move_camera(phi=90*DEGREES, theta=90*DEGREES, zoom=1.75, run_time=3.5)
        self.wait(2)
        self.play(Create(flux_arrow))  # Mostra o vetor E explicitamente
        self.wait()

        # --- ROTAÇÕES COM INDICADOR VISUAL DO ÂNGULO ---
        self.play(angle_tracker.animate.set_value(PI/4), run_time=7, rate_func=smooth)
        self.wait()
        self.play(FadeIn(angle_group))  # Mostra as linhas e o arco do ângulo
        self.play(angle_tracker.animate.set_value(PI/2), run_time=7, rate_func=smooth)
        self.wait()
        self.play(angle_tracker.animate.set_value(3*PI/4), run_time=7, rate_func=smooth)
        self.wait(2)
        self.play(angle_tracker.animate.set_value(PI), run_time=7, rate_func=smooth)
        self.wait(2)
        self.play(FadeOut(angle_group))  # Remove o indicador visual
        self.wait(2)

        # --- REMOÇÃO DO VETOR DE FLUXO ---
        self.play(FadeOut(flux_arrow))
        self.wait()

        # --- MUDANÇA DE VISTA DA CÂMERA ---
        self.move_camera(phi=60*DEGREES, theta=30*DEGREES, zoom=1.75, run_time=3.5)

        # --- ROTAÇÃO FINAL COM CAMPO VETORIAL ---
        self.play(FadeIn(vector_field))
        self.begin_ambient_camera_rotation(rate=0.1)  # Inicia uma rotação suave e contínua da câmera
        self.wait(15)  # Mantém a animação por 15 segundos
        


