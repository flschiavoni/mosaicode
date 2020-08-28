from tests.mosaicode_tests.test_base import TestBase
from mosaicode.control.codegenerator import CodeGenerator


class TestCodeGenerator(TestBase):

    def test_constructor(self):
        self.code_generator = CodeGenerator(None)
        diagram = self.create_diagram()
        self.code_generator = CodeGenerator(diagram)

        diagram = self.create_diagram()
        diagram.code_template = None
        self.code_generator = CodeGenerator(diagram)

        diagram = self.create_diagram()
        diagram.language = None
        self.code_generator = CodeGenerator(diagram)

    def test_generate_code(self):
        diagram = self.create_diagram()
        self.code_generator = CodeGenerator(diagram)
        self.code_generator.generate_code()

        diagram.code_template = None
        self.code_generator.generate_code()

        diagram = self.create_full_diagram()
        self.code_generator = CodeGenerator(diagram)
        self.code_generator.generate_code()

