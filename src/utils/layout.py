import networkx as nx
import numpy as np
import scipy as sp

def fruchterman_reingold(G: nx.DiGraph, iterations: int = 50):
    pos_arr = None
    dom_size = 1

    if len(G) == 0:
        return {}
    if len(G) == 1:
        return {nx.utils.arbitrary_element(G.nodes()): np.array([0.0, 0.0])}

    try:
        if len(G) < 500:
            raise ValueError
        A = nx.to_scipy_sparse_array(G, dtype='f', weight='weight')
        pos = _sparse_fruchterman_reingold(A, iterations=iterations)
    except ValueError:
        A = nx.to_numpy_array(G, dtype='f', weight='weight')
        nnodes, _ = A.shape
        k = dom_size / np.sqrt(nnodes)
        pos = _fruchterman_reingold(A, k, pos_arr, iterations = iterations)
    pos = dict(zip(G, pos))
    return pos


def _fruchterman_reingold(A, k=None, pos=None, fixed=None, iterations=50):
    try:
        nnodes, _ = A.shape
    except AttributeError as err:
        msg = "fruchterman_reingold() takes an adjacency matrix as input"
        raise nx.NetworkXError(msg) from err

    if pos is None:
        # random initial positions
        pos = np.asarray(np.random.rand(nnodes, 2), dtype=A.dtype)
    else:
        pos = pos.astype(A.dtype)

    if k is None:
        k = np.sqrt(1.0 / nnodes)
    t = max(max(pos.T[0]) - min(pos.T[0]), max(pos.T[1]) - min(pos.T[1])) * 0.1
    dt = t / (iterations + 1)
    delta = np.zeros((pos.shape[0], pos.shape[0], pos.shape[1]), dtype=A.dtype)
    for iteration in range(iterations):
        delta = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
        distance = np.linalg.norm(delta, axis=-1)
        np.clip(distance, 0.01, None, out=distance)
        displacement = np.einsum(
            "ijk,ij->ik", delta, (k * k / distance**2 - A * distance / k)
        )
        length = np.linalg.norm(displacement, axis=-1)
        length = np.where(length < 0.01, 0.1, length)
        delta_pos = np.einsum("ij,i->ij", displacement, t / length)
        if fixed is not None:
            delta_pos[fixed] = 0.0
        pos += delta_pos
        t -= dt
    return pos

def _sparse_fruchterman_reingold(A, k=None, iterations=100):
    # Sparse version

    try:
        nnodes, _ = A.shape
    except AttributeError as err:
        msg = "fruchterman_reingold() takes an adjacency matrix as input"
        raise nx.NetworkXError(msg) from err
    try:
        A = A.tolil()
    except AttributeError:
        A = (sp.sparse.coo_array(A)).tolil()

    pos = np.asarray(np.random.rand(nnodes, 2), dtype=A.dtype)
    fixed = []
    k = np.sqrt(1.0 / nnodes)
    t = max(max(pos.T[0]) - min(pos.T[0]), max(pos.T[1]) - min(pos.T[1])) * 0.1
    dt = t / (iterations + 1)

    displacement = np.zeros((2, nnodes))
    for iteration in range(iterations):
        displacement *= 0
        # loop over rows
        for i in range(A.shape[0]):
            if i in fixed:
                continue
            delta = (pos[i] - pos).T
            distance = np.sqrt((delta**2).sum(axis=0))
            distance = np.where(distance < 0.01, 0.01, distance)
            Ai = A.getrowview(i).toarray()
            displacement[:, i] += (
                delta * (k * k / distance**2 - Ai * distance / k)
            ).sum(axis=1)
        length = np.sqrt((displacement**2).sum(axis=0))
        length = np.where(length < 0.01, 0.1, length)
        delta_pos = (displacement * t / length).T
        pos += delta_pos
        t -= dt
    return pos


def rescale_layout(pos, width, height, margin=10):
    positions_array = np.array(list(pos.values()))

    min_coords = positions_array.min(axis=0)
    max_coords = positions_array.max(axis=0)
    positions_array -= min_coords

    max_canvas_size = np.array([width - 2 * margin, height - 2 * margin])
    scale = min(max_canvas_size / (max_coords - min_coords))
    positions_array *= scale

    offset = (max_canvas_size - (positions_array.max(axis=0) - positions_array.min(axis=0))) / 2
    positions_array += offset + margin

    new_pos = {node: (pos_tuple[0], pos_tuple[1]) for node, pos_tuple in zip(pos.keys(), positions_array)}
    return new_pos
