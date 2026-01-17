# ANIMAÇÃO 4: Fluxo do campo elétrico gerado por uma partícula carregada em uma superfície gaussiana genérica
from manim import *
from manim_physics import *
import numpy as np
import random 

class carga_2D(Scene):
    def construct(self):
        # ============================================================
        # 1. DEFINIÇÃO DAS SUPERFÍCIES GAUSSIANAS
        # ============================================================
        
        # Função que define uma curva polar complexa
        def r(theta):
            """
            Define uma função polar complexa para criar uma superfície
            gaussiana com forma não-trivial, demonstrando que a Lei de Gauss
            vale para qualquer superfície fechada, independente da forma.
            """
            return np.sin(theta)**3 + np.cos(theta)**3
        
        # Criação de uma superfície fechada complexa em 3D (mas no plano z=0)
        close_surface = Surface(
            # Função paramétrica que define a superfície complexa
            lambda u, v: np.array([
                r(u) * np.cos(u) * np.cos(v),  # Coordenada x
                r(u) * np.sin(u) * np.cos(v),  # Coordenada y
                0                              # Coordenada z (mantém no plano XY)
            ]),
            u_range=[0, TAU],      # Ângulo polar completo (0 a 2π)
            v_range=[0, PI / 2],   # Segundo parâmetro para criar volume/espessura
            resolution=(30,30),    # Resolução da malha (alta para visualização suave)
            fill_color=BLUE,       # Cor de preenchimento azul
            fill_opacity=0.2,      # Baixa opacidade para ver linhas de campo
            stroke_color=BLUE,     # Cor das linhas da grade
            stroke_width=0.01,     # Linhas muito finas
        )
        # Transformações visuais aplicadas à superfície
        close_surface.scale(5)                     # Ampliação para preencher cena
        close_surface.rotate(-7*PI/4)              # Rotação inicial para melhor apresentação
        close_surface.set_z_index(-5)              # Coloca no fundo da cena
        
        # Criação de uma superfície retangular simples (prisma fino) como alternativa
        sq = Prism([4.5, 3.2, 0]).set_stroke(WHITE).set_opacity(0.2)
        sq.set_z_index(-5)  # Também posicionado no fundo
        
        # ============================================================
        # 2. DEFINIÇÃO DAS CARGAS ELÉTRICAS
        # ============================================================
        
        e = 1.6  # Valor da carga elementar (em unidades arbitrárias para visualização)
        
        # Grupo para a carga positiva (+2e)
        carga_positiva = VGroup()        
        positive_charge = Charge(
            magnitude=+2*e,  # Carga positiva com magnitude 2 vezes a carga elementar
            color=RED        # Vermelho convencional para cargas positivas
        )
        # Rótulo "+" sobre a carga para identificação visual
        charge_label_pos = Tex("+", color=WHITE, font_size=24).next_to(positive_charge, ORIGIN)
        charge_label_pos.set_z_index(+5)  # Garante visibilidade na frente de outros objetos
        carga_positiva.add(positive_charge, charge_label_pos)  # Agrupa carga e rótulo
         
        # Grupo para a primeira carga negativa (-2e)
        carga_negativa = VGroup()  
        negative_charge = Charge(
            magnitude=-2*e,  # Carga negativa com magnitude -2e
            color=BLUE       # Azul convencional para cargas negativas
        )
        charge_label_neg = Tex("-", color=WHITE, font_size=24).next_to(negative_charge, ORIGIN)
        charge_label_neg.set_z_index(+5)
        carga_negativa.add(negative_charge, charge_label_neg)
        
        # Grupo para a segunda carga negativa (-2e) com posição inicial diferente
        carga_negativa_2 = VGroup()        
        negative_charge_2 = Charge(
            magnitude=-2*e,     # Mesma magnitude que a primeira carga negativa
            point=RIGHT*1.7,    # Posição inicial à direita da origem
            color=BLUE
        )
        charge_label_neg_2 = Tex("-", color=WHITE, font_size=24).next_to(negative_charge_2, ORIGIN)
        charge_label_neg_2.set_z_index(+5).shift(RIGHT*1.7)  # Ajuste de posição do rótulo
        carga_negativa_2.add(negative_charge_2, charge_label_neg_2)
        
        # Grupo do dipolo (cargas positiva e negativa próximas)
        di_pole = VGroup(negative_charge, positive_charge)
      
        # ============================================================
        # 3. DEFINIÇÃO DOS CAMPOS ELÉTRICOS
        # ============================================================
        
        # Campo elétrico da primeira carga negativa individual
        field_neg = always_redraw(lambda: ElectricField(negative_charge))
        # Atualiza automaticamente se a carga se mover
        
        # Campo elétrico do sistema triplo (três cargas)
        field_neg_2 = always_redraw(lambda: ElectricField(positive_charge, negative_charge, negative_charge_2))
        # Mostra o campo resultante da superposição de três cargas
    
        # Campo elétrico da carga positiva individual
        field_pos = always_redraw(lambda: ElectricField(positive_charge))
       
        # Campo elétrico do dipolo (duas cargas de magnitudes iguais e opostas)
        field_di = always_redraw(lambda: ElectricField(positive_charge, negative_charge))
        # Representa o campo de um dipolo elétrico
    
        # ============================================================
        # 4. FUNÇÕES PERSONALIZADAS PARA CÁLCULO DE CAMPOS VETORIAIS
        # ============================================================
        
        # Função para campo elétrico radial de uma carga pontual na origem
        def radial_field(p):
            """
            Calcula o campo elétrico radial de uma carga pontual localizada na origem.
            
            Física: Lei de Coulomb - E ∝ 1/r² na direção radial.
            
            Parâmetros:
            p: ponto no espaço (array numpy [x, y, z])
            
            Retorna:
            Vetor campo elétrico no ponto p
            """
            r = np.linalg.norm(p)  # Distância do ponto à origem
            if r < 0.1:            # Evita divisão por zero próximo à origem
                return np.zeros(3)
            return p / (r**3)      # Campo proporcional a 1/r² na direção radial
        
        # Função para campo elétrico de um dipolo
        def dipole_field(p):
            """
            Calcula o campo elétrico total de um dipolo usando o princípio de superposição.
            Um dipolo consiste em duas cargas iguais e opostas separadas por uma distância.
            
            Parâmetros:
            p: ponto onde calcular o campo
            
            Retorna:
            Soma vetorial dos campos individuais das duas cargas
            """
            # Campo da carga positiva
            r_pos = p - carga_positiva.get_center()  # Vetor da carga positiva ao ponto
            dist_pos = np.linalg.norm(r_pos)         # Distância até a carga positiva
            if dist_pos < 0.1:                       # Evita singularidade
                field_pos = np.zeros(3)
            else:
                field_pos = r_pos / (dist_pos**3)    # Campo aponta para fora da carga positiva
            
            # Campo da carga negativa
            r_neg = p - carga_negativa.get_center()  # Vetor da carga negativa ao ponto
            dist_neg = np.linalg.norm(r_neg)         # Distância até a carga negativa
            if dist_neg < 0.1:                       # Evita singularidade
                field_neg = np.zeros(3)
            else:
                # Sinal negativo inverte a direção (campo aponta para a carga negativa)
                field_neg = -r_neg / (dist_neg**3)
            
            # Campo total: superposição dos campos individuais
            return field_pos + field_neg
        
        # ============================================================
        # 5. LINHAS DE FLUXO PARA VISUALIZAÇÃO ALTERNATIVA
        # ============================================================
        
        # Linhas de fluxo para o campo dipolar
        stream_lines_dipole = StreamLines(
            dipole_field,           # Função do campo a ser visualizado
            stroke_width=0.8,       # Espessura das linhas de fluxo
            n_repeats=5,            # Número de linhas a serem geradas
            virtual_time=4,         # Tempo de simulação para cada linha
            max_anchors_per_line=4, # Número máximo de pontos de ancoragem por linha
            dt=1.0,                 # Passo de integração para traçar linhas
        )
        # Nota: Estas stream lines são definidas mas não usadas na animação principal
        
        # Linhas de fluxo para campo radial
        stream_lines_radial = StreamLines(
            radial_field,
            stroke_width=1.5,
            n_repeats=2,
            virtual_time=10,
            max_anchors_per_line=5,
            dt=5,                    # Passo maior para simulação mais suave
        )
        # Nota: Também definidas mas não usadas
        
        # ============================================================
        # 6. SEQUÊNCIA PRINCIPAL DE ANIMAÇÕES
        # ============================================================
        
        # A. Introdução da superfície gaussiana complexa
        self.play(FadeIn(close_surface))
        self.wait()
        
        # B. Apresentação da carga positiva isolada e seu campo radial
        self.play(LaggedStart(
            Create(carga_positiva),   # Animação de criação da carga
            FadeIn(field_pos),        # Apresentação gradual do campo elétrico
            lag_ratio=0.05            # Pequeno atraso entre as duas animações
        ))
        self.wait()  # Pausa para observação
        
        # C. Remove o campo para preparar transição de configuração
        self.play(FadeOut(field_pos))
        self.wait()  # Pausa entre transições
   
        # D. Substitui carga positiva por carga negativa
        self.play(LaggedStart(
            FadeOut(carga_positiva),           # Desaparecimento suave da carga positiva
            FadeIn(carga_negativa, field_neg), # Aparecimento simultâneo da carga negativa e seu campo
            lag_ratio=0.1                      # Atraso um pouco maior entre os efeitos
        ))        
        self.wait()  # Pausa para observação da nova configuração
        
        # E. Transição entre superfícies gaussianas (complexa → retangular)
        self.play(LaggedStart(
            FadeOut(close_surface),  # Remoção da superfície complexa
            lag_ratio=0.1
        ), run_time=2)  # Duração mais longa para transição suave
        
        # F. Introdução da superfície retangular simples
        self.play(FadeIn(sq), run_time=2)
        self.wait()  # Pausa para observação da nova superfície
        
        # G. Move a carga negativa para dentro da superfície retangular
        self.play(carga_negativa.animate.shift(RIGHT*1.7), run_time=2)
        self.wait(3)  # Pausa mais longa para observação
        
        # H. Destaque visual da superfície gaussiana (fluxo não nulo)
        self.play(Circumscribe(sq, fade_in=True, fade_out=True))
        self.wait(3)  # Pausa após o destaque
        
        # I. Move a carga para fora da superfície (canto superior direito)
        self.play(carga_negativa.animate.shift(UR*2.5), run_time=2)
        self.wait(3)  # Pausa para observação
        
        # J. Destaque da superfície novamente (agora com fluxo nulo - carga fora)
        self.play(Circumscribe(sq, fade_in=True, fade_out=True))
        self.wait(4)  # Pausa mais longa para enfatizar o conceito
        
        # K. Sequência de movimentos demonstrativos da carga
        # Mostra como o fluxo é nulo quando a carga está fora da superfície,
        # independentemente da direção ou distância
        
        # Move para esquerda (fora da superfície)
        self.play(carga_negativa.animate.shift(LEFT*7.2), run_time=2)
        self.wait()  # Pausa breve
        
        # Move para baixo (fora da superfície)
        self.play(carga_negativa.animate.shift(DOWN*6.2), run_time=2)
        self.wait()  # Pausa breve
        
        # Move para direita (fora da superfície)
        self.play(carga_negativa.animate.shift(RIGHT*6.2), run_time=2)
        self.wait()  # Pausa breve
        
        # Retorna ao centro (origem) - dentro da superfície
        self.play(carga_negativa.animate.move_to(ORIGIN), run_time=2)
        self.wait(2)  # Pausa final para observação
