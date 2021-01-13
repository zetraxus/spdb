from backend.categories_dict import categories


class SQLQuery:
    def __init__(self, request):
        self.category = request.form.get('category')
        self.longitude = request.form.get('longitude')
        self.latitude = request.form.get('latitude')
        self.rev_cnt = request.form.get('rev_cnt')
        self.min_rating = request.form.get('min_rating')
        self.min_price = request.form.get('min_price')
        self.max_price = request.form.get('max_price')
        self.address = request.form.get('address')
        self.distance = request.form.get('distance')
        self.results_cnt = request.form.get('results_cnt')
        self.order = request.form.get('order')

        if self.distance:
            self.distance = int(self.distance)
        else:
            self.distance = 1000

        if self.results_cnt:
            self.results_cnt = int(self.results_cnt)
        else:
            self.results_cnt = 20

    def build_sql_query(self):
        conditions = []
        if self.category:
            cond = "main_category in ("
            for cat in [x.strip() for x in self.category.split(',')]:
                if cat in categories.keys():
                    for category in categories[cat]:
                        cond += '\'' + category + '\','
            cond = cond[:-1] + ')'
            conditions.append(cond)
        if self.rev_cnt:
            conditions.append("review_count >= " + self.rev_cnt)
        if self.min_rating:
            conditions.append("rating >= " + self.min_rating)
        if self.min_price:
            cond = "(price = ' ' or price >= '"
            for i in range(len(self.min_price)):
                cond += "$"
            cond += '\')'
            conditions.append(cond)
        if self.max_price:
            cond = "(price = ' ' or price <= '"
            for i in range(len(self.max_price)):
                cond += "$"
            cond += '\')'
            conditions.append(cond)

        query = "select * from restaurants_test"
        if conditions:
            query += " where "
            for cond in conditions:
                query += cond + " and "
            query = query[:-5]
        query += ';'
        return query
