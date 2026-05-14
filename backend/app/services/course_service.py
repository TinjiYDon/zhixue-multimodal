from app.schemas.course import CourseCreate, CourseRead

_in_memory: list[CourseRead] = []


async def list_courses() -> list[CourseRead]:
    return list(_in_memory)


async def create_course(body: CourseCreate) -> CourseRead:
    new_id = str(len(_in_memory) + 1)
    item = CourseRead(id=new_id, title=body.title)
    _in_memory.append(item)
    return item
