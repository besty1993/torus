import numpy as np
import pandas as pd

class Render():
    def __init__(self, light_vector=(1,1,1), window_size=(70,35)):
        self.setProjPlane(0,0,1)
        self.setLightVector(*light_vector)
        self.window_size = window_size

    def __call__(self, points, norms):
        ## The inner surface of cylinder get disappeared
        # points, norms = self.filterByNormalVectors(points, norms)

        proj = self.project(points)
        proj = self.fitToWindow(proj)
        bright = self.computeBrightness(norms)

        proj, bright = self.filterByDistance(points, proj, bright)
        
        return self.print(proj, bright)

    def setProjPlane(self, *args):
        assert len(args) == 3

        norm = np.linalg.norm([*args])
        assert norm > 0
        
        self.plane_vec = np.array([*args])
        self.plane_vec = self.plane_vec / norm

    def setLightVector(self, *args):
        assert len(args) == 3

        norm = np.linalg.norm([*args])
        assert norm > 0
        
        self.light_vec = np.array([*args])
        self.light_vec = self.light_vec / norm

    def computeBrightness(self, normal_vectors):
        return np.dot(normal_vectors, self.light_vec)

    def filterByNormalVectors(self, points, norms):
        inners = np.dot(norms, self.plane_vec)
        points = points[inners>=0]
        norms = norms[inners>=0]
        return points, norms

    def project(self, vectors):
        """
        project to xy plane
        """
        z_sizes = np.dot(vectors, self.plane_vec)[:, np.newaxis]
        z_vecs = np.dot(z_sizes, self.plane_vec[np.newaxis,:])
        projected = (vectors - z_vecs)[:,:2]
        return projected

    def fitToWindow(self, vectors):
        window = np.array(self.window_size)
        vectors = (vectors+1)*(window//2)
        vectors = vectors.astype(np.int)
        return vectors

    def print(self, vectors, brightness):
        text = [(' '*(self.window_size[0]+1))]*(self.window_size[1]+1)
        for i, point in enumerate(vectors):
            x = point[0]; y = point[1]
            text[y] = list(text[y])
            b = brightness[i]
            
            if b > 0.8:
                text[y][x]='@'
            elif b > 0.6:
                text[y][x]='$'
            elif b > 0.4:
                text[y][x]='|'
            elif b > 0.2:
                text[y][x]='+'
            elif b > 0.1:
                text[y][x]='-'
            else:
                text[y][x]='·'

            text[y] = ''.join(text[y])
        return np.array(text)


    @classmethod
    def move(cls, points, x_dist, y_dist, z_dist):
        points += np.array([x_dist, y_dist, z_dist])
        return points

    @classmethod
    def rotate(cls, vectors, x_rot, y_rot, z_rot):
        x_matrix = np.array([
            [1,                     0,                     0],
            [0,       np.cos(x_rot),  (-1)*np.sin(x_rot)],
            [0,       np.sin(x_rot),       np.cos(x_rot)],
        ])
        y_matrix = np.array([
            [np.cos(y_rot),       0,       np.sin(y_rot)],
            [0,                     1,                     0],
            [(-1)*np.sin(y_rot),  0,       np.cos(y_rot)]
        ])
        z_matrix = np.array([
            [np.cos(z_rot),       (-1)*np.sin(z_rot),  0],
            [np.sin(z_rot),       np.cos(z_rot),       0],
            [0,                     0,                     1]
        ])
        new_vectors = np.dot(vectors, x_matrix)
        new_vectors = np.dot(new_vectors, y_matrix)
        new_vectors = np.dot(new_vectors, z_matrix)
        return new_vectors

    @classmethod
    def getDuplicateIdxs(cls, proj):
        """
        Get duplicate indices 
        """
        df = pd.DataFrame(proj).copy()
        df[0] = 1000*df[0]+df[1]
        return df.groupby([0]).indices

    @classmethod
    def filterByDistance(cls, points, proj, bright):
        """
        When the rendered object is printed on the window,
        only one point per window grid is needed.
        So, if there are several points that will be printed on same grid,
        select only one point which is the farthest from the projection plane.
        Since object is projected on XY-plane, z value is the distance between the projection plane and the point.
        Once the object is projected, only the point with the longest distance should be remained.
        """
        filtered_proj = []
        filtered_bright = []

        dups_list = cls.getDuplicateIdxs(proj)
        for dups in dups_list.values():
            if len(dups) == 1:
                idx = dups[0]
            else:
                z_dists = points[dups,2]
                idx = dups[np.argmax(z_dists)]
            filtered_proj.append(proj[idx])
            filtered_bright.append(bright[idx])

        filtered_proj = np.array(filtered_proj)
        filtered_bright = np.array(filtered_bright)

        return filtered_proj, filtered_bright