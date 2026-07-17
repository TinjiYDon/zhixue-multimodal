from app.schemas.course import CourseCreate, CourseRead

_in_memory: list[CourseRead] = []


async def list_courses() -> list[CourseRead]:
    return list(_in_memory)


async def create_course(body: CourseCreate) -> CourseRead:
    new_id = str(len(_in_memory) + 1)
    item = CourseRead(id=new_id, title=body.title)
    _in_memory.append(item)
    return item


# 新增：根据id获取单条课程
async def get_course(course_id: str) -> CourseRead | None:
    for item in _in_memory:
        if item.id == course_id:
            return item
    return None


# 新增：修改课程标题
async def update_course(course_id: str, new_title: str) -> CourseRead | None:
    for idx, item in enumerate(_in_memory):
        if item.id == course_id:
            updated = CourseRead(id=item.id, title=new_title)
            _in_memory[idx] = updated
            return updated
    return None


# 新增：删除课程
async def delete_course(course_id: str) -> bool:
    global _in_memory
    before_len = len(_in_memory)
    _in_memory = [item for item in _in_memory if item.id != course_id]
    return len(_in_memory) < before_len