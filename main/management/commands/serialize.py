import simplejson
import redis
import math

FOR_ROW = 1
FOR_COLUMN = 2


def sparse_vector_to_hash(vec):
    all_items = {}
    nonzero = vec.nonzero()
    shape = vec.shape
    if shape[0] > shape[1]:  # column
        direction = FOR_ROW
    else:
        direction = FOR_COLUMN

    if nonzero:
        for coords in zip(vec.nonzero()[0], vec.nonzero()[1]):
            if FOR_COLUMN == direction:  # row number of values
                all_items[str(coords[0])] = str(vec[coords[0], coords[1]])
            else:  # column number f values
                all_items[str(coords[1])] = str(vec[coords[0], coords[1]])
    return all_items


def sparse_vector_to_json(vec):
    return simplejson.dumps(sparse_vector_to_hash(vec))


def redis_prefix(matrix_id):
    return "matrix:" + str(matrix_id) + ":"


def redis_row_key(matrix_id, row_id):
    return redis_prefix(matrix_id) + "row:" + str(row_id)


def redis_column_key(matrix_id, column_id):
    return redis_prefix(matrix_id) + "column:" + str(column_id)


def export_sparse_matrix(matrix, matrix_id):
    row_matrix = matrix.tocsr()
    column_matrix = matrix.tocsc()
    redis_conn = redis.Redis()
    redis_conn.set(redis_prefix(matrix_id) + ":num_rows", matrix.shape[0])
    redis_conn.set(redis_prefix(matrix_id) + ":num_columns", matrix.shape[1])

    for row_id in range(row_matrix.shape[0]):
        redis_conn.set(redis_row_key(matrix_id, row_id),
                       sparse_vector_to_json(matrix[row_id, :]))

    for column_id in range(column_matrix.shape[1]):
        redis_conn.set(redis_column_key(matrix_id, column_id),
                       sparse_vector_to_json(matrix[:, column_id]))


class StreamingIterator:

    def __init__(self, matrix, concurrency):
        self._matrix = matrix
        self._concurrency = concurrency
        linear_buckets = math.sqrt(self._concurrency)
        self._row_width = matrix.shape[0] / linear_buckets
        self._column_width = matrix.shape[1] / linear_buckets

    def next(self):
        return 1
