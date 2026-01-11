# ANIMAÇÃO 4: Fluxo do campo elétrico gerado por uma partícula carregada em uma superfície gaussiana genérica
from manim import *
from manim_physics import *
import numpy as np
import random 

class charge_gauss_2D_dipole(Scene):
    def construct(self):
        # ============================================================
        # 1. DEFINIÇÃO DAS SUPERFÍCIES GAUSSIANAS
        # ============================================================
        
        # Função que define a forma da superfície fechada (curva r(θ))
        def r(theta):
            """
            Define uma curva polar complexa para a superfície gaussiana.
            Esta forma não é uma figura geométrica simples, criando uma
            superfície fechada interessante para visualização.
            """
            return np.sin(theta)**3 + np.cos(theta)**3
        
        # Criação da superfície fechada complexa usando parametrização 3D
        close_surface = Surface(
            lambda u, v: np.array([
                r(u) * np.cos(u) * np.cos(v),  # Coordenada x
                r(u) * np.sin(u) * np.cos(v),  # Coordenada y
                0                              # Coordenada z (plano XY)
            ]),
            u_range=[0, TAU],      # Ângulo θ varia de 0 a 2π (volta completa)
            v_range=[0, PI / 2],   # Parâmetro v para criar espessura
            resolution=(30,30),    # Resolução da malha (alta para suavidade)
            fill_color=BLUE,       # Cor de preenchimento azul
            fill_opacity=0.25,     # Transparência para ver através
            stroke_color=BLUE,     # Cor das linhas da grade
            stroke_width=0.01,     # Espessura fina das linhas
        )
        # Ajustes visuais da superfície
        close_surface.scale(5)                     # Ampliação para melhor visualização
        close_surface.rotate(-7*PI/4)              # Rotação inicial
        close_surface.set_z_index(-5)              # Coloca no fundo da cena
        
        # Criação de uma superfície retangular simples (prisma fino)
        sq = Prism([4.5, 3.2, 0]).set_stroke(WHITE).set_opacity(0.25)
        sq.set_z_index(-5)  # Também no fundo
        
        # ============================================================
        # 2. DEFINIÇÃO DAS CARGAS ELÉTRICAS
        # ============================================================
        
        e = 1.6  # Valor da carga elementar (em unidades arbitrárias)
        
        # Grupo para a carga positiva (+2e)
        carga_positiva = VGroup()        
        positive_charge = Charge(
            magnitude=+2*e,  # Carga positiva com magnitude 2e
            color=RED        # Vermelho para carga positiva
        )
        charge_label_pos = Tex("+", color=WHITE, font_size=24).next_to(positive_charge, ORIGIN)
        charge_label_pos.set_z_index(+5)  # Frente de outros objetos
        carga_positiva.add(positive_charge, charge_label_pos)
         
        # Grupo para a primeira carga negativa (-2e)
        carga_negativa = VGroup()  
        negative_charge = Charge(
            magnitude=-2*e,  # Carga negativa com magnitude -2e
            color=BLUE       # Azul para carga negativa
        )
        charge_label_neg = Tex("-", color=WHITE, font_size=24).next_to(negative_charge, ORIGIN)
        charge_label_neg.set_z_index(+5)
        carga_negativa.add(negative_charge, charge_label_neg)
        
        # Grupo para a segunda carga negativa (-3.5e)
        carga_negativa_2 = VGroup()        
        negative_charge_2 = Charge(
            magnitude=-3.5*e,    # Carga negativa com magnitude diferente
            point=RIGHT*1.7,     # Posição inicial diferente
            color=BLUE
        )
        charge_label_neg_2 = Tex("-", color=WHITE, font_size=24).next_to(negative_charge_2, ORIGIN)
        charge_label_neg_2.set_z_index(+5)
        carga_negativa_2.add(negative_charge_2, charge_label_neg_2)
        
        # Grupo do dipolo (par de cargas positiva e negativa)
        di_pole = VGroup(negative_charge, positive_charge)
      
        # ============================================================
        # 3. DEFINIÇÃO DOS CAMPOS ELÉTRICOS
        # ============================================================
        
        # Campo da primeira carga negativa (sempre atualizado)
        field_neg = always_redraw(lambda: ElectricField(negative_charge))
        
        # Campo da segunda carga negativa (sempre atualizado)
        field_neg_2 = always_redraw(lambda: ElectricField(negative_charge_2))

        # Campo da carga positiva (sempre atualizado)
        field_pos = always_redraw(lambda: ElectricField(positive_charge))
       
        # Campo do dipolo (entre as duas cargas)
        field_di = always_redraw(lambda: ElectricField(positive_charge, negative_charge))
        
        # Campo do sistema triplo (três cargas)
        field_tri = always_redraw(lambda: ElectricField(positive_charge, negative_charge, negative_charge_2))
    
        # ============================================================
        # 4. FUNÇÕES PERSONALIZADAS PARA CAMPOS VETORIAIS
        # ============================================================
        
        # Função para campo elétrico radial (carga pontual isolada)
        def radial_field(p):
            """
            Calcula o campo elétrico radial de uma carga pontual na origem.
            
            Parâmetros:
            p: ponto no espaço (array numpy [x, y, z])
            
            Retorna:
            Vetor do campo elétrico no ponto p
            """
            r = np.linalg.norm(p)  # Distância da origem
            if r < 0.1:            # Evita divisão por zero perto da origem
                return np.zeros(3)
            return p / (r**3)      # Campo proporcional a 1/r² (direção radial)
        
        # Função para campo elétrico de um dipolo
        def dipole_field(p):
            """
            Calcula o campo elétrico total de um dipolo.
            
            O dipolo consiste em uma carga positiva e uma negativa
            separadas por uma distância.
            """
            # Campo da carga positiva
            r_pos = p - carga_positiva.get_center()
            dist_pos = np.linalg.norm(r_pos)
            if dist_pos < 0.1:
                field_pos = np.zeros(3)
            else:
                field_pos = r_pos / (dist_pos**3)  # Campo apontando para fora
            
            # Campo da carga negativa
            r_neg = p - carga_negativa.get_center()
            dist_neg = np.linalg.norm(r_neg)
            if dist_neg < 0.1:
                field_neg = np.zeros(3)
            else:
                field_neg = -r_neg / (dist_neg**3)  # Sinal negativo para carga negativa
            
            # Campo total (soma vetorial)
            return field_pos + field_neg
        
        # ============================================================
        # 5. LINHAS DE FLUXO (STREAM LINES) PARA VISUALIZAÇÃO
        # ============================================================
        
        # Linhas de fluxo para o campo do dipolo
        stream_lines_dipole = StreamLines(
            dipole_field,
            stroke_width=0.8,      # Espessura das linhas
            n_repeats=5,           # Número de linhas geradas
            virtual_time=4,        # Tempo virtual de integração
            max_anchors_per_line=4,# Pontos de ancoragem por linha
            dt=1.0,                # Passo de integração
        )
        
        # Linhas de fluxo para campo radial
        stream_lines_radial = StreamLines(
            radial_field,
            stroke_width=1.5,
            n_repeats=2,
            virtual_time=10,
            max_anchors_per_line=5,
            dt=5,  # Passo de integração maior para campo mais suave
        )
        
        # ============================================================
        # 6. SEQUÊNCIA PRINCIPAL DE ANIMAÇÕES
        # ============================================================
        
        # A. Introdução da superfície retangular
        self.play(FadeIn(sq))
        self.wait()
               
        # B. Animação da primeira carga negativa
        self.play(LaggedStart(
            FadeIn(carga_negativa),
            carga_negativa.animate.shift(RIGHT*1.7),  # Move para posição final
            lag_ratio=0.3
        ))
        self.wait()    
        
        # C. Animação da carga positiva
        self.play(LaggedStart(
            FadeIn(carga_positiva),
            carga_positiva.animate.shift(LEFT*1.7),  # Move para posição final
            lag_ratio=0.3
        ))
        self.wait(2)
        
        # D. Introdução do campo do dipolo
        self.play(FadeIn(field_di))
        self.wait(3)

        # E. Destaque da superfície gaussiana
        self.play(Circumscribe(sq, fade_in=True, fade_out=True))
        self.wait(5)
        
        # F. Transição para sistema triplo (adiciona terceira carga)
        self.play(LaggedStart(
            FadeOut(field_di),
            FadeIn(carga_negativa_2),
            carga_negativa_2.animate.shift(UR*1.8),  # Move para canto superior direito
            lag_ratio=0.5
        ))
        self.wait(2)
        
        # G. Introdução do campo do sistema triplo
        self.play(FadeIn(field_tri))
        self.wait(5)
        
        # H. Transição para campo de carga negativa isolada
        self.play(FadeOut(field_tri))
        self.play(LaggedStart(
            FadeOut(carga_negativa, carga_positiva),
            FadeIn(field_neg_2),
            lag_ratio=0.5
        ))
        self.wait(3)
        
        # I. Novamente destaca a superfície gaussiana
        self.play(Circumscribe(sq, fade_in=True, fade_out=True))
        self.wait(5)
        
        # J. Retorno ao sistema triplo completo
        self.play(FadeOut(field_neg_2))
        self.play(LaggedStart(
            FadeIn(carga_negativa, carga_positiva),
            FadeIn(field_tri),
            lag_ratio=0.5
        ))
        self.wait(3)