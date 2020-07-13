import imagematrix


'''

dp:

.213.
..x..

'''


class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        dp = {}
        p = {}
        for y in range(self.height):
            for x in range(self.width):
                opts = [(x, y - 1), (x - 1, y - 1), (x + 1, y - 1)]
                best_e, best_p = (0, None) if y == 0 else min(
                    map(
                        lambda x: (dp.get(x, float('inf')), x),
                        opts,
                    )
                )
                dp[x, y] = best_e + self.energy(x, y)
                p[x, y] = best_p

        min_e = float('inf')
        min_x = None
        for x in range(self.width):
            e = dp[x, self.height - 1]
            if e < min_e:
                min_e = e
                min_x = x

        path = []
        c = (min_x, self.height - 1)
        while c:
            path.append(c)
            c = p[c]
        path.reverse()
        return path

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
