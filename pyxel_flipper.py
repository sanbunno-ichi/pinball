#pymunkのfripper.pyをpyxelで再現
import pyxel

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
INIT_POS = SCREEN_WIDTH//2+20, SCREEN_HEIGHT//4
BALL_RADIUS = 20

class App:
	def __init__( self, pymunk, fps=60 ):
		self.pymunk = pymunk
		self.fps = fps

		pyxel.init( SCREEN_WIDTH, SCREEN_HEIGHT, fps=fps, title="pyxel flipper" )
		self.create_world()
		pyxel.run(self.update, self.draw)

	def create_world(self):
		self.space = self.pymunk.Space()
		self.space.gravity = ( 0.0, 900.0 )
		self.space.sleep_time_threshold = 0.3

		#外壁
		static_lines = [
			pymunk.Segment(self.space.static_body, (150, 500), (50, 50), 1.0),
			pymunk.Segment(self.space.static_body, (450, 500), (550, 50), 1.0),
			pymunk.Segment(self.space.static_body, (50, 50), (300, 0), 1.0),
			pymunk.Segment(self.space.static_body, (300, 0), (550, 50), 1.0),
			pymunk.Segment(self.space.static_body, (300, 180), (400, 200), 1.0),
		]
		for line in static_lines:
			line.elasticity = 0.7
			line.group = 1
		self.space.add(*static_lines)

		#フリッパー
		fp = [(20, -20), (-120, 0), (20, 20)]
		mass = 100
		moment = pymunk.moment_for_poly(mass, fp)

		# right flipper
		self.r_flipper_body = pymunk.Body(mass, moment)
		self.r_flipper_body.position = 450, 500
		self.r_flipper_shape = pymunk.Poly(self.r_flipper_body, fp)
		self.space.add(self.r_flipper_body, self.r_flipper_shape)

		self.r_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
		self.r_flipper_joint_body.position = self.r_flipper_body.position
		j = pymunk.PinJoint(self.r_flipper_body, self.r_flipper_joint_body, (0, 0), (0, 0))
		s = pymunk.DampedRotarySpring(
			self.r_flipper_body, self.r_flipper_joint_body, 0.15, 20000000, 900000
		)
		self.space.add(j, s)

		# left flipper
		self.l_flipper_body = pymunk.Body(mass, moment)
		self.l_flipper_body.position = 150, 500
		self.l_flipper_shape = pymunk.Poly(self.l_flipper_body, [(-x, y) for x, y in fp])
		self.space.add(self.l_flipper_body, self.l_flipper_shape)

		self.l_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
		self.l_flipper_joint_body.position = self.l_flipper_body.position
		j = pymunk.PinJoint(self.l_flipper_body, self.l_flipper_joint_body, (0, 0), (0, 0))
		s = pymunk.DampedRotarySpring(
			self.l_flipper_body, self.l_flipper_joint_body, -0.15, 20000000, 900000
		)
		self.space.add(j, s)

		self.r_flipper_shape.group = self.l_flipper_shape.group = 1
		self.r_flipper_shape.elasticity = self.l_flipper_shape.elasticity = 0.4

		#バンパー
		self.bumper1_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
		self.bumper1_body.position = (240, 100)
		self.bumper1_shape = pymunk.Circle( self.bumper1_body, 10 )
		self.bumper1_shape.elasticity = 1.5
		self.space.add(self.bumper1_body, self.bumper1_shape)

		self.bumper2_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
		self.bumper2_body.position = (360, 100)
		self.bumper2_shape = pymunk.Circle( self.bumper2_body, 10 )
		self.bumper2_shape.elasticity = 1.5
		self.space.add( self.bumper2_body, self.bumper2_shape )

		#ボール
		self.ball_body = pymunk.Body( 1, float('inf') )
		self.ball_body.position = ( INIT_POS )
		self.ball_shape = pymunk.Circle( self.ball_body, BALL_RADIUS )
		self.ball_shape.elasticity = 0.9
		self.space.add( self.ball_body, self.ball_shape )

	def update(self):
		step = 5
		step_dt = 1 / self.fps / step
		for _ in range(step):
			self.space.step(step_dt)

		#操作
		if self.getInputB():
			pyxel.quit()

		# 左フリッパーの制御
		if self.getInputLEFT():  # キーを押している間、フリッパーを上げる
			self.l_flipper_body.apply_impulse_at_local_point(
				Vec2d.unit() * 8000, (-100, 0)
			)
		# 右フリッパーの制御
		if self.getInputRIGHT():  # キーを押している間、フリッパーを上げる
			self.r_flipper_body.apply_impulse_at_local_point(
				Vec2d.unit() * -8000, (-100, 0)
			)

		#ボールが画面外になったかどうかの判定
		if self.ball_body.position.get_distance((300, 300)) > 1000:
			self.ball_body.position = INIT_POS
			self.ball_body.velocity = (0, 0)


	def draw(self):
		pyxel.cls(0)

		#外壁
		pyxel.line( 150, 500, 50, 50, 7 )
		pyxel.line( 450, 500, 550, 50, 7 )
		pyxel.line( 50, 50, 300, 0, 7 )
		pyxel.line( 300, 0, 550, 50, 7 )
		pyxel.line( 300, 180, 400, 200, 7 )

		#フリッパー
		self.r_flipper_body.position = 450, 500
		self.l_flipper_body.position = 150, 500
		self.r_flipper_body.velocity = self.l_flipper_body.velocity = 0, 0

		_x = [0,0,0]
		_y = [0,0,0]

		_cnt = 0
		for v in self.r_flipper_shape.get_vertices():
			_x[_cnt],_y[_cnt] = v.rotated(self.r_flipper_shape.body.angle) + self.r_flipper_shape.body.position
			_cnt += 1

		pyxel.tri(_x[0],_y[0],_x[1],_y[1],_x[2],_y[2],6)

		_cnt = 0
		for v in self.l_flipper_shape.get_vertices():
			_x[_cnt],_y[_cnt] = v.rotated(self.l_flipper_shape.body.angle) + self.l_flipper_shape.body.position
			_cnt += 1

		pyxel.tri(_x[0],_y[0],_x[1],_y[1],_x[2],_y[2],6)


		#バンパー
		x, y = self.bumper1_body.position
		pyxel.circ( x, y, 10, 11 )
		x, y = self.bumper2_body.position
		pyxel.circ( x, y, 10, 11 )

		#ボール
		x, y = self.ball_body.position
		pyxel.circ( x, y, BALL_RADIUS, 14 )


	#-----------------------------------------------------------------
	#入力（キーボード＆ジョイパッド）
	#-----------------------------------------------------------------
	#左
	def getInputLEFT(self):
		if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
			return 1
		else:
			return 0
	#右
	def getInputRIGHT(self):
		if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
			return 1
		else:
			return 0
	#button-A
	def getInputA(self):
		if pyxel.btnp(pyxel.KEY_Z, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A, hold=10, repeat=10):
			return 1
		else:
			return 0
	#button-B
	def getInputB(self):
		if pyxel.btnp(pyxel.KEY_X, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B, hold=10, repeat=10):
			return 1
		else:
			return 0


if __name__ == "__main__":
	import pymunk
	from pymunk import Vec2d

	FPS = 60
	App(pymunk, FPS)
