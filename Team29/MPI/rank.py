from util import zero_in_degree


def rank_by_total_successors(framework):

    def set_ranks():
        for task in zero_in_degree(framework.dag):
            rank(task)

    def rank(task):
        if task._rank is not None:
            return task._rank

        r = 0
        for successor in framework.dag.successors_iter(task):
            r -= rank(successor)
            r -= 1
        task._rank = r
        return r

    set_ranks()
