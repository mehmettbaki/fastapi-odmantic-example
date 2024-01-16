from typing import List, Optional

from fastapi import FastAPI, HTTPException

from odmantic import AIOEngine, Model, ObjectId


class Tree(Model):
    name: str
    average_size: Optional[float] = None
    discovery_year: int


app = FastAPI()

engine = AIOEngine()


@app.post("/trees/", response_model=Tree)
async def postTree(tree: Tree):
    async with engine.session() as session:
        await session.save(tree)
        return tree


@app.get("/trees/", response_model=List[Tree])
async def get_trees():
    async with engine.session() as session:
        trees = await session.find(Tree)
        return trees


@app.get("/trees/count", response_model=int)
async def count_trees():
    async with engine.session() as session:
        count = await session.count(Tree)
        return count


@app.get("/trees/{id}", response_model=Tree)
async def get_tree_by_id(id: ObjectId):
    async with engine.session() as session:
        tree = await session.find_one(Tree, Tree.id == id)
        if tree is None:
            raise HTTPException(404)
        return tree


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, port=8080)
