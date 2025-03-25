class PaginationHelper:

    @staticmethod
    def apply_pagination(query, page: int, size: int):
        return query.offset((page - 1) * size).limit(size)
