from fastapi import APIRouter

# Import routers from all modules
from brain_v2.modules.knowledge.router import router as knowledge_router
from brain_v2.modules.memory.router import router as memory_router
from brain_v2.modules.reasoning.router import router as reasoning_router
from brain_v2.modules.decision.router import router as decision_router
from brain_v2.modules.planning.router import router as planning_router
from brain_v2.modules.task.router import router as task_router
from brain_v2.modules.project.router import router as project_router
from brain_v2.modules.execution.router import router as execution_router
from brain_v2.modules.learning.router import router as learning_router
from brain_v2.modules.mrm_connector.router import router as mrm_connector_router

api_router = APIRouter(prefix="/api/v1")

# Include all module routers
api_router.include_router(knowledge_router)
api_router.include_router(memory_router)
api_router.include_router(reasoning_router)
api_router.include_router(decision_router)
api_router.include_router(planning_router)
api_router.include_router(task_router)
api_router.include_router(project_router)
api_router.include_router(execution_router)
api_router.include_router(learning_router)
api_router.include_router(mrm_connector_router)