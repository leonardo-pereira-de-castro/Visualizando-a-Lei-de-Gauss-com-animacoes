# ANIMAÇÃO 2: Fluxo do campo elétrico através de uma superfície fechada
from manim import *
import numpy as np
import math

class cubic_flux(ThreeDScene):
    def construct(self):
        # ============================================
        # 1. CONFIGURAÇÃO INICIAL DA CENA
        # ============================================
        
        # Define a orientação inicial da câmera (ângulos phi e theta)
        self.set_camera_orientation(phi=60*DEGREES, theta=45*DEGREES)
        
        # ============================================
        # 2. CRIAÇÃO DO CUBO
        # ============================================
        
        # Cria um prisma com dimensões 2x2x2 (um cubo) e posiciona na origem
        cube = Prism(dimensions=[2, 2, 2]).move_to(ORIGIN)
        # Define a cor de preenchimento, opacidade e borda
        cube.set_fill(BLUE, 0.5)
        cube.set_stroke(WHITE, 1)
        cube.set_opacity(0.3)
        cube.set_z_index(+3)  # Garante que o cubo fique na frente de outros objetos
        
        # Anima a entrada do cubo na cena
        self.play(FadeIn(cube))
        self.wait(2)
        # Reduz a opacidade do cubo para destacar outros elementos posteriormente
        self.play(cube.animate.set_opacity(0.1))
        self.wait(2)
        
        # ============================================
        # 3. FUNÇÃO PARA DESTACAR PARES DE FACES E MOSTRAR VETORES NORMAIS
        # ============================================
        
        # Função que destaca duas faces do cubo e anima a aparição dos vetores normais
        def highlight_pair(face1, face2):
            # Destaca as bordas das faces
            face1.set_stroke(WHITE, 2)
            face2.set_stroke(WHITE, 2)
            # Anima o preenchimento das faces com uma cor mais opaca
            self.play(
                face1.animate.set_fill(BLUE, 0.5),
                face2.animate.set_fill(BLUE, 0.5)
            )

            # Função interna para calcular o vetor normal de uma face
            def get_normal(face):
                # Obtém os vértices da face (os três primeiros vértices definem um plano)
                vertices = face.get_vertices()
                # Calcula dois vetores no plano da face
                v1 = np.array(vertices[1]) - np.array(vertices[0])
                v2 = np.array(vertices[2]) - np.array(vertices[0])
                # O produto vetorial dá o vetor normal (não normalizado)
                normal = np.cross(v1, v2)
                # Retorna o vetor normal unitário
                return normal / np.linalg.norm(normal)

            # Calcula os vetores normais para as duas faces
            normal1 = get_normal(face1)
            normal2 = get_normal(face2)
            
            # Cria setas 3D para representar os vetores normais (apontando para dentro do cubo)
            vec1 = Arrow3D(
                start=face1.get_center(),
                end=face1.get_center() - 1.5*normal1,  # O vetor é escalado por 1.5
                color=WHITE
            )
            
            vec2 = Arrow3D(
                start=face2.get_center(),
                end=face2.get_center() - 1.5*normal2,
                color=WHITE
            )

            # Anima a entrada dos vetores normais
            self.play(FadeIn(vec1, vec2))
      
            # Remove os vetores normais e restaura a aparência original das faces
            self.play(FadeOut(vec1, vec2))
            self.play(
                face1.animate.set_fill(BLUE, 0.5).set_stroke(WHITE, 1),
                face2.animate.set_fill(BLUE, 0.5).set_stroke(WHITE, 1)
            )

        # ============================================
        # 4. SEQUÊNCIA DE DESTAQUE DOS PARES DE FACES OPOSTAS
        # ============================================
        
        # Lista de pares de faces (índices do cubo). Cada par são faces opostas.
        pairs = [(0, 1), (2, 3), (4, 5)]
        for i, j in pairs:
            highlight_pair(cube[i], cube[j])
            self.wait(0.5)

        # ============================================
        # 5. MUDANÇA DE ÂNGULO DA CÂMERA
        # ============================================
        
        # Move a câmera para uma vista de topo (phi=90, theta=90)
        self.move_camera(phi=90*DEGREES, theta=90*DEGREES, run_time=3)
        self.wait()
        
        # ============================================
        # 6. CRIAÇÃO DO CAMPO VETORIAL UNIFORME
        # ============================================
        
        # Função que cria um vetor do campo em um ponto (x, y, z)
        def create_vector(x, y, z):
            direction = np.array([2.0, 0.0, 0.0])/2.3  # Direção constante (eixo x) e tamanho ajustado
            start_point = np.array([x, y, z])
            end_point = start_point + direction
            arrow = Arrow3D(
                start=start_point,
                end=end_point,
                color=RED,
                thickness=0.01,
                resolution=6,  # Número de segmentos para suavizar a seta
            )
            return arrow

        # Define intervalos para criar uma grade 3D de vetores
        x_range = np.arange(-3.75, 3.75, 1.0)
        y_range = np.arange(-2.0, 2.0, 1.5)
        z_range = np.arange(-1.0, 2.0, 1.0)

        # Grupo para armazenar todos os vetores do campo
        vector_field = VGroup()

        # Cria os vetores em cada ponto da grade
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    vector_field.add(create_vector(x, y, z))

        # Função para atualizar a visibilidade dos vetores (opacidade) com base na posição relativa ao cubo
        def update_visibility(mobject):
            for arrow in vector_field:
                start = arrow.get_start()
                # Verifica se o vetor está dentro do cubo
                if (
                    -1.0 <= start[0] <= 1.0 and
                    -1.0 <= start[1] <= 1.0 and
                    -1.0 <= start[2] <= 1.0
                ):
                    arrow.set_opacity(0.3)  # Mais transparente se estiver dentro do cubo
                else:
                    arrow.set_opacity(0.8)  # Mais visível se estiver fora do cubo

        # Conecta a função de atualização ao campo vetorial (será chamada a cada frame)
        vector_field.add_updater(update_visibility)
        
        # Adiciona o campo vetorial à cena
        self.play(FadeIn(vector_field, run_time=2))
        self.wait(5)
                
        # ============================================
        # 7. FUNÇÃO PARA MOSTRAR VETORES NORMAIS SEM RÓTULOS (repetida para ênfase)
        # ============================================
        
        def norma_vector_faces(face1,face2):
            # Função interna para calcular o vetor normal (igual à anterior)
            def get_normal(face):
                vertices = face.get_vertices()
                v1 = np.array(vertices[1]) - np.array(vertices[0])
                v2 = np.array(vertices[2]) - np.array(vertices[0])
                normal = np.cross(v1, v2)
                return normal / np.linalg.norm(normal)

            # Calcula os vetores normais
            normal1 = get_normal(face1)
            normal2 = get_normal(face2)
            
            # Cria as setas 3D
            vec1 = Arrow3D(
                start=face1.get_center(),
                end=face1.get_center() - 1.5*normal1,
                color=WHITE
            )
            
            vec2 = Arrow3D(
                start=face2.get_center(),
                end=face2.get_center() - 1.5*normal2,
                color=WHITE
            )

            # Anima a entrada dos vetores, um por um
            self.play(FadeIn(vec1))
            self.wait()
            self.play(FadeIn(vec2))
            self.wait()
            
            # Remove os vetores
            self.play(FadeOut(vec1, vec2))
            
        
        # ============================================
        # 8. MUDANÇA DE CÂMERA E DESTAQUE DE PARES DE FACES COM COR DIFERENTE
        # ============================================
        
        # Ajusta a câmera para uma nova perspectiva
        self.move_camera(phi=60*DEGREES, theta=60*DEGREES, run_time=3)
        self.wait(2)
        
        # Função similar à highlight_pair, mas com cor amarela e animação sequencial dos vetores
        def highlight_pair_without_label(face1, face2):
            face1.set_stroke(WHITE, 2)
            face2.set_stroke(WHITE, 2)
            self.play(
                face1.animate.set_fill(YELLOW_A, 0.5),
                face2.animate.set_fill(YELLOW_A, 0.5)
            )

            # Função para calcular o vetor normal (igual às anteriores)
            def get_normal(face):
                vertices = face.get_vertices()
                v1 = np.array(vertices[1]) - np.array(vertices[0])
                v2 = np.array(vertices[2]) - np.array(vertices[0])
                normal = np.cross(v1, v2)
                return normal / np.linalg.norm(normal)

            normal1 = get_normal(face1)
            normal2 = get_normal(face2)
            
            vec1 = Arrow3D(
                start=face1.get_center(),
                end=face1.get_center() - 1.5*normal1,
                color=WHITE
            )
            
            vec2 = Arrow3D(
                start=face2.get_center(),
                end=face2.get_center() - 1.5*normal2,
                color=WHITE
            )

            # Anima a entrada dos vetores separadamente
            self.play(FadeIn(vec1))
            self.wait()
            self.play(FadeIn(vec2))
            self.wait()
            
            # Remove os vetores e restaura a aparência original das faces
            self.play(FadeOut(vec1, vec2))
            self.play(
                face1.animate.set_fill(BLUE, 0.5).set_stroke(WHITE, 1),
                face2.animate.set_fill(BLUE, 0.5).set_stroke(WHITE, 1)
            )

        # Destaca dois pares de faces opostas (índices 0-1 e 2-3)
        pairs = [(0, 1), (2, 3)]
        for i, j in pairs:
            highlight_pair_without_label(cube[i], cube[j])
            self.wait(0.5)
        
        # ============================================
        # 9. ROTAÇÃO SUAVE DA CÂMERA E FINALIZAÇÃO
        # ============================================
        
        # Inicia uma rotação contínua da câmera para dar uma visão dinâmica da cena
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(10)
        
        # Remove o campo vetorial e o cubo
        self.play(FadeOut(vector_field))
        self.wait()
        
        # Finaliza removendo o cubo
        self.play(FadeOut(cube))

        
