# test_structure.py
from memory_system import CompanionMemory, CompanionMemoryWithChroma

print("✅ Base class exists:", CompanionMemory)
print("✅ Child class exists:", CompanionMemoryWithChroma)

# Test instantiation
try:
    base_memory = CompanionMemory()
    enhanced_memory = CompanionMemoryWithChroma()
    print("✅ Both classes can be instantiated successfully!")
except Exception as e:
    print(f"❌ Error: {e}")