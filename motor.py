import numpy as np
import matplotlib.pyplot as plt
import vg
import math


def vector_creator(p1, p2):
    return p2-p1


def norm_vector(vector):
    return vector / np.linalg.norm(vector)


def angle(v1, v2):
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)

    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def proj_rpy(vector):

    i = np.array([1.0, 0.0, 0.0])
    j = np.array([0.0, 1.0, 0.0])
    k = np.array([0.0, 0.0, 1.0])

    proj_p = vector - ((np.dot(vector, i)/np.linalg.norm(i)**2) * i)
    proj_r = vector - ((np.dot(vector, j)/np.linalg.norm(j)**2) * j)
    proj_j = vector - ((np.dot(vector, k)/np.linalg.norm(k)**2) * k)

    return proj_p, proj_r, proj_j


def movement_motor(m_1, m_2, m_3, m_4, speeds, mod_spd, m1_speed, m2_speed, m3_speed, m4_speed):

    m_1.speed = speeds[0]
    m_2.speed = speeds[1]
    m_3.speed = speeds[2]
    m_4.speed = speeds[3]
    m_1.modify_speed(mod_spd)
    m_2.modify_speed(mod_spd)
    m_3.modify_speed(mod_spd)
    m_4.modify_speed(mod_spd)

    m1_speed.append(m_1.speed)
    m2_speed.append(m_2.speed)
    m3_speed.append(m_3.speed)
    m4_speed.append(m_4.speed)

    return m1_speed, m2_speed, m3_speed, m4_speed


def speed_state(**kwargs):
    motor_1 = kwargs['motor_1']
    motor_2 = kwargs['motor_2']
    motor_3 = kwargs['motor_3']
    motor_4 = kwargs['motor_4']
    x_v = kwargs['x_v']
    list_of_vectors = kwargs['list_of_vectors']

    stay = [2.0, 2.0, 2.0, 2.0]
    fwd = [2.0, 2.0, 3.0, 3.0]
    bwd = [3.0, 3.0, 2.0, 2.0]
    jcw = [3.0, 2.0, 2.0, 3.0]
    jccw = [2.0, 3.0, 3.0, 2.0]

    m1 = [0.0]
    m2 = [0.0]
    m3 = [0.0]
    m4 = [0.0]

    i = np.array([1.0, 0.0, 0.0])
    j = np.array([0.0, 1.0, 0.0])
    k = np.array([0.0, 0.0, 1.0])

    # STAY
    m1, m2, m3, m4 = movement_motor(motor_1, motor_2, motor_3, motor_4, stay, 'None', m1, m2, m3, m4)

    for m in range(x_v):
        current_vector = list_of_vectors[m]
        if np.sum(current_vector) == 1:
            # print('Movement in a single axis')
            if np.all(current_vector == i):
                # print('Rotation -90 Needed')
                m1, m2, m3, m4 = movement_motor(motor_1, motor_2, motor_3, motor_4, jcw, 'None', m1, m2, m3, m4)
                m1, m2, m3, m4 = movement_motor(motor_1, motor_2, motor_3, motor_4, fwd, 'None', m1, m2, m3, m4)
            elif np.all(current_vector == j):
                # print('Movement Forward')
                m1, m2, m3, m4 = movement_motor(motor_1, motor_2, motor_3, motor_4, fwd, 'None', m1, m2, m3, m4)
            elif np.all(current_vector == k):
                # print('Elevate')
                m1, m2, m3, m4 = movement_motor(motor_1, motor_2, motor_3, motor_4, stay, 'Up', m1, m2, m3, m4)

        elif np.sum(current_vector) == -1:
            # print('Movement in a single axis, negative')
            if np.all(current_vector == -1 * i):
                # print('Rotation 90 Needed')
                m1, m2, m3, m4 = movement_motor(motor_1, motor_2, motor_3, motor_4, jccw, 'None', m1, m2, m3, m4)
                m1, m2, m3, m4 = movement_motor(motor_1, motor_2, motor_3, motor_4, fwd, 'None', m1, m2, m3, m4)
            elif np.all(current_vector == -1 * j):
                # print('Movement Backward')
                m1, m2, m3, m4 = movement_motor(motor_1, motor_2, motor_3, motor_4, bwd, 'None', m1, m2, m3, m4)
            elif np.all(current_vector == -1 * k):
                # print('Descent')
                m1, m2, m3, m4 = movement_motor(motor_1, motor_2, motor_3, motor_4, stay, 'Down', m1, m2, m3, m4)

        else:
            previous_vector = list_of_vectors[m - 1]
            xx = vg.signed_angle(j, current_vector, look=vg.basis.x)  # PITCH
            # YY = vg.signed_angle(previous_vector, current_vector, look=vg.basis.y) # ROLL
            zz = vg.signed_angle(previous_vector, current_vector, look=vg.basis.z)  # JAW
            zz_num = float(zz)

            if not math.isnan(zz_num):
                spin = jcw if zz_num > 0.0 else jccw
                m1, m2, m3, m4 = movement_motor(motor_1, motor_2, motor_3, motor_4, spin, 'None', m1, m2, m3, m4)
                rot_vect = vg.rotate(current_vector, k, -1.0 * zz_num)
                xx = vg.signed_angle(j, rot_vect, look=vg.basis.x)

            xx_num = float(xx)
            if 0.0 < xx_num <= 90.0:
                mod, direction = ['Up', fwd]
            elif 90.0 < xx_num <= 180.0:
                mod, direction = ['Up', bwd]
            elif -90.0 < xx_num <= 0.0:
                mod, direction = ['Down', fwd]
            elif -180.0 < xx_num <= -90.0:
                mod, direction = ['Down', fwd]
            else:
                mod, direction = ['Up', fwd]

            m1, m2, m3, m4 = movement_motor(motor_1, motor_2, motor_3, motor_4, direction, mod, m1, m2, m3, m4)

    m1, m2, m3, m4 = movement_motor(motor_1, motor_2, motor_3, motor_4, stay, 'None', m1, m2, m3, m4)

    # PLOT STATE OF MOTORS #
    x_p = np.arange(np.shape(m1)[0])

    fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4, constrained_layout=True)

    ax0.scatter(x_p, m1)
    ax0.plot(x_p, m1)
    ax0.set_title('Motor 1')
    ax0.set_ylabel('Velocidad')
    ax1.scatter(x_p, m2)
    ax1.plot(x_p, m2)
    ax1.set_title('Motor 2')
    ax1.set_ylabel('Velocidad')
    ax2.scatter(x_p, m3)
    ax2.plot(x_p, m3)
    ax2.set_title('Motor 3')
    ax2.set_ylabel('Velocidad')
    ax3.scatter(x_p, m4)
    ax3.plot(x_p, m4)
    ax3.set_title('Motor 4')
    ax3.set_ylabel('Velocidad')
    plt.show()


class Motor:
    def __init__(self, motor, speed, mod):
        self.motor = motor
        self.speed = speed
        self.mod = mod

    def modify_speed(self, mod):
        if mod == 'Up':
            self.speed = 4
        elif mod == 'Down':
            self.speed = 1
        else:
            self.speed = self.speed
