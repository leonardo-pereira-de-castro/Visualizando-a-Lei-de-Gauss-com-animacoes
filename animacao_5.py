# ANIMAÇÃO 5: Fluxo do campo elétrico gerado por um dipolo elétrico em uma superfície gaussiana genérica
from manim import *
from manim_physics import *
import numpy as np
import random 

class dipolo_2D(Scene):
    def construct(self):
        # ============================================================
        # 1. DEFINIÇÃO DAS SUPERFÍCIES GAUSSIANAS
        # ============================================================
        
        # Função que define uma forma complexa em coordenadas polares
        def r(theta):
            """
            Define uma curva polar complexa para criar uma superfície
            gaussiana com forma não-trivial, demonstrando que a Lei de Gauss
            vale para qualquer superfície fechada.
            """
            return np.sin(theta)**3 + np.cos(theta)**3
        
        # Criação de superfície fechada complexa (não usada diretamente na animação)
        close_surface = Surface(
            lambda u, v: np.array([
                r(u) * np.cos(u) * np.cos(v),  # Coordenada x
                r(u) * np.sin(u) * np.cos(v),  # Coordenada y
                0                              # Coordenada z (plano XY)
            ]),
            u_range=[0, TAU],      # Ângulo polar completo (0 a 2π)
            v_range=[0, PI / 2],   # Parâmetro para criar espessura
            resolution=(30,30),    # Alta resolução para visualização suave
            fill_color=BLUE,       # Cor de preenchimento
            fill_opacity=0.25,     # Transparência para ver linhas de campo
            stroke_color=BLUE,     # Cor das linhas da grade
            stroke_width=0.01,     # Linhas finas
        )
        # Transformações visuais da superfície complexa
        close_surface.scale(5)                     # Aumenta tamanho para preencher cena
        close_surface.rotate(-7*PI/4)              # Rotação estética inicial
        close_surface.set_z_index(-5)              # Coloca no fundo
        
        # Superfície retangular simples (prisma fino) - superfície gaussiana principal
        sq = Prism([4.5, 3.2, 0]).set_stroke(WHITE).set_opacity(0.25)
        sq.set_z_index(-5)  # Também no fundo
        
        # ============================================================
        # 2. DEFINIÇÃO DAS CARGAS ELÉTRICAS
        # ============================================================
        
        e = 1.6  # Valor da carga elementar (unidades arbitrárias)
        
        # Grupo para a carga positiva (+2e)
        carga_positiva = VGroup()        
        positive_charge = Charge(
            magnitude=+2*e,  # Carga positiva com magnitude 2e
            color=RED        # Vermelho para cargas positivas
        )
        # Rótulo "+" sobre a carga
        charge_label_pos = Tex("+", color=WHITE, font_size=24).next_to(positive_charge, ORIGIN)
        charge_label_pos.set_z_index(+5)  # Na frente de outros objetos
        carga_positiva.add(positive_charge, charge_label_pos)
         
        # Grupo para a primeira carga negativa (-2e)
        carga_negativa = VGroup()  
        negative_charge = Charge(
            magnitude=-2*e,  # Carga negativa com magnitude -2e
            color=BLUE       # Azul para cargas negativas
        )
        charge_label_neg = Tex("-", color=WHITE, font_size=24).next_to(negative_charge, ORIGIN)
        charge_label_neg.set_z_index(+5)
        carga_negativa.add(negative_charge, charge_label_neg)
        
        # Grupo para a segunda carga negativa (-3.5e) - magnitude diferente
        carga_negativa_2 = VGroup()        
        negative_charge_2 = Charge(
            magnitude=-3.5*e,    # Carga negativa com magnitude maior
            point=RIGHT*1.7,     # Posição inicial à direita
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
        
        # Campo da primeira carga negativa individual
        field_neg = always_redraw(lambda: ElectricField(negative_charge))
        
        # Campo da segunda carga negativa individual
        field_neg_2 = always_redraw(lambda: ElectricField(negative_charge_2))

        # Campo da carga positiva individual
        field_pos = always_redraw(lambda: ElectricField(positive_charge))
       
        # Campo do dipolo (entre as duas cargas)
        field_di = always_redraw(lambda: ElectricField(positive_charge, negative_charge))
        
        # Campo do sistema triplo (três cargas)
        field_tri = always_redraw(lambda: ElectricField(positive_charge, negative_charge, negative_charge_2))
    
        # ============================================================
        # 4. FUNÇÕES PERSONALIZADAS PARA CÁLCULO DE CAMPOS
        # ============================================================
        
        # Função para campo elétrico radial (carga pontual na origem)
        def radial_field(p):
            """
            Calcula campo elétrico de uma carga pontual na origem.
            Segue a lei de Coulomb: E ∝ 1/r² na direção radial.
            
            Parâmetros:
            p: ponto no espaço (array 3D)
            
            Retorna:
            Vetor campo elétrico no ponto p
            """
            r = np.linalg.norm(p)  # Distância do ponto à origem
            if r < 0.1:            # Evita divisão por zero próximo à origem
                return np.zeros(3)
            return p / (r**3)      # Lei de Coulomb: E ∝ 1/r²
        
        # Função para campo elétrico de um dipolo
        def dipole_field(p):
            """
            Calcula campo elétrico total de um dipolo usando superposição.
            Mostra como campos de múltiplas cargas se combinam.
            """
            # Campo da carga positiva
            r_pos = p - carga_positiva.get_center()
            dist_pos = np.linalg.norm(r_pos)
            if dist_pos < 0.1:
                field_pos = np.zeros(3)
            else:
                field_pos = r_pos / (dist_pos**3)  # Campo que aponta para fora
            
            # Campo da carga negativa
            r_neg = p - carga_negativa.get_center()
            dist_neg = np.linalg.norm(r_neg)
            if dist_neg < 0.1:
                field_neg = np.zeros(3)
            else:
                # Sinal negativo inverte direção (campo aponta para dentro)
                field_neg = -r_neg / (dist_neg**3)
            
            # Campo total (soma vetorial dos campos individuais)
            return field_pos + field_neg
        
        # ============================================================
        # 5. LINHAS DE FLUXO PARA VISUALIZAÇÃO ALTERNATIVA
        # ============================================================
        
        # Linhas de fluxo para o campo do dipolo
        stream_lines_dipole = StreamLines(
            dipole_field,           # Função do campo
            stroke_width=0.8,       # Espessura das linhas
            n_repeats=5,            # Número de linhas
            virtual_time=4,         # Tempo de simulação
            max_anchors_per_line=4, # Pontos de ancoragem
            dt=1.0,                 # Passo de integração
        )
        
        # Linhas de fluxo para campo radial
        stream_lines_radial = StreamLines(
            radial_field,
            stroke_width=1.5,
            n_repeats=2,
            virtual_time=10,
            max_anchors_per_line=5,
            dt=5,                   # Passo maior para maior suavidade
        )
        
        # ============================================================
        # 6. SEQUÊNCIA PRINCIPAL DE ANIMAÇÕES
        # ============================================================
        
        # A. Introdução da superfície retangular
        self.play(FadeIn(sq))
        self.wait()
               
        # B. Animação da primeira carga negativa (move para posição)
        self.play(LaggedStart(
            FadeIn(carga_negativa),
            carga_negativa.animate.shift(RIGHT*1.7),  # Move para direita
            lag_ratio=0.3  # Pequeno atraso entre os dois efeitos
        ))
        self.wait()    
        
        # C. Animação da carga positiva (move para posição oposta)
        self.play(LaggedStart(
            FadeIn(carga_positiva),
            carga_positiva.animate.shift(LEFT*1.7),  # Move para esquerda
            lag_ratio=0.3
        ))
        self.wait(2)
        
        # D. Introdução do campo do dipolo
        self.play(FadeIn(field_di))
        self.wait(3)

        # E. Destaque da superfície gaussiana (fluxo do dipolo)
        self.play(Circumscribe(sq, fade_in=True, fade_out=True))
        self.wait(5)
        
        # F. Transição para sistema triplo (adiciona terceira carga)
        self.play(LaggedStart(
            FadeOut(field_di),                    # Remove campo do dipolo
            FadeIn(carga_negativa_2),             # Adiciona terceira carga
            carga_negativa_2.animate.shift(UR*1.8),  # Move para canto superior direito
            lag_ratio=0.5
        ))
        self.wait(2)
        
        # G. Introdução do campo do sistema triplo
        self.play(FadeIn(field_tri))
        self.wait(5)
        
        # H. Transição para apenas uma carga negativa (sistema simplificado)
        self.play(FadeOut(field_tri))
        self.play(LaggedStart(
            FadeOut(carga_negativa, carga_positiva),  # Remove duas cargas
            FadeIn(field_neg_2),                      # Mostra campo da carga restante
            lag_ratio=0.5
        ))
        self.wait(3)
        
        # I. Destaque da superfície com apenas uma carga
        self.play(Circumscribe(sq, fade_in=True, fade_out=True))
        self.wait(5)
        
        # J. Retorno ao sistema triplo completo
        self.play(FadeOut(field_neg_2))
        self.play(LaggedStart(
            FadeIn(carga_negativa, carga_positiva),  # Restaura duas cargas removidas
            FadeIn(field_tri),                       # Restaura campo triplo
            lag_ratio=0.5
        ))

        self.wait(3)
