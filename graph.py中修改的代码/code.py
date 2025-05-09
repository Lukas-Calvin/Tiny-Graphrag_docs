    def get_topk_similar_entities(self, query_emb, k=1) -> List[Node]:
        res = []
        query = """
        MATCH (n)
        RETURN n
        """ 
        with self.driver.session() as session:
            result = list(session.run(query))# 相比于原代码，仅此行代码不同，一次将数据读取到内存，防止多次读取，但仅适用于小数据集。使用原代码会出现：ResultConsumedError: The result has been consumed. Fetch all needed records before calling Result.consume().的报错
        for record in result:
            node = record["n"]
            if node["embedding"] is not None:
                similarity = cosine_similarity(query_emb, node["embedding"])
                node_obj = Node(
                    name=node["name"],
                    desc=node["description"],
                    chunks_id=node["chunks_id"],
                    entity_id=node["entity_id"],
                    similarity=similarity
                )
                res.append(node_obj)
        return sorted(res, key=lambda x: x.similarity, reverse=True)[:k]
