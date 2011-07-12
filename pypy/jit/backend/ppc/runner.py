import py
from pypy.rpython.lltypesystem import lltype, llmemory, rffi
from pypy.rpython.lltypesystem.lloperation import llop
from pypy.rpython.llinterp import LLInterpreter
from pypy.rlib.objectmodel import we_are_translated
from pypy.jit.metainterp import history, compile
from pypy.jit.backend.x86.assembler import Assembler386
from pypy.jit.backend.x86.arch import FORCE_INDEX_OFS
from pypy.jit.backend.x86.profagent import ProfileAgent
from pypy.jit.backend.llsupport.llmodel import AbstractLLCPU
from pypy.jit.backend.x86 import regloc
import sys

from pypy.tool.ansi_print import ansi_log
log = py.log.Producer('jitbackend')
py.log.setconsumer('jitbackend', ansi_log)


class PPC_64_CPU(AbstractLLCPU):
    debug = True
    supports_floats = False

    BOOTSTRAP_TP = lltype.FuncType([], lltype.Signed)
    dont_keepalive_stuff = False # for tests

    def __init__(self, rtyper, stats, opts=None, translate_support_code=False,
                 gcdescr=None):
        if gcdescr is not None:
            gcdescr.force_index_ofs = FORCE_INDEX_OFS
        AbstractLLCPU.__init__(self, rtyper, stats, opts,
                               translate_support_code, gcdescr)

    def setup(self):
        if self.opts is not None:
            failargs_limit = self.opts.failargs_limit
        else:
            failargs_limit = 1000
        self.assembler = Assembler386(self, self.translate_support_code,
                                            failargs_limit)

    def get_on_leave_jitted_hook(self):
        return self.assembler.leave_jitted_hook

    def setup_once(self):
        self.assembler.setup_once()

    def finish_once(self):
        self.assembler.finish_once()

    def compile_loop(self, inputargs, operations, looptoken, log=True):
        return self.assembler.assemble_loop(inputargs, operations, looptoken,
                                            log=log)

    def compile_bridge(self, faildescr, inputargs, operations,
                       original_loop_token, log=True):
        clt = original_loop_token.compiled_loop_token
        clt.compiling_a_bridge()
        return self.assembler.assemble_bridge(faildescr, inputargs, operations,
                                              original_loop_token, log=log)

    def set_future_value_int(self, index, intvalue):
        self.assembler.fail_boxes_int.setitem(index, intvalue)

    def set_future_value_float(self, index, floatvalue):
        self.assembler.fail_boxes_float.setitem(index, floatvalue)

    def set_future_value_ref(self, index, ptrvalue):
        self.assembler.fail_boxes_ptr.setitem(index, ptrvalue)

    def get_latest_value_int(self, index):
        return self.assembler.fail_boxes_int.getitem(index)

    def get_latest_value_float(self, index):
        return self.assembler.fail_boxes_float.getitem(index)

    def get_latest_value_ref(self, index):
        return self.assembler.fail_boxes_ptr.getitem(index)

    def get_latest_value_count(self):
        return self.assembler.fail_boxes_count

    def clear_latest_values(self, count):
        setitem = self.assembler.fail_boxes_ptr.setitem
        null = lltype.nullptr(llmemory.GCREF.TO)
        for index in range(count):
            setitem(index, null)

    def get_latest_force_token(self):
        return self.assembler.fail_ebp + FORCE_INDEX_OFS

    def execute_token(self, executable_token):
        addr = executable_token._x86_bootstrap_code
        #llop.debug_print(lltype.Void, ">>>> Entering", addr)
        func = rffi.cast(lltype.Ptr(self.BOOTSTRAP_TP), addr)
        #llop.debug_print(lltype.Void, "<<<< Back")
        fail_index = self._execute_call(func)
        return self.get_fail_descr_from_number(fail_index)

    def _execute_call(self, func):
        # help flow objspace
        prev_interpreter = None
        if not self.translate_support_code:
            prev_interpreter = LLInterpreter.current_interpreter
            LLInterpreter.current_interpreter = self.debug_ll_interpreter
        res = 0
        try:
            res = func()
        finally:
            if not self.translate_support_code:
                LLInterpreter.current_interpreter = prev_interpreter
        return res

    @staticmethod
    def cast_ptr_to_int(x):
        adr = llmemory.cast_ptr_to_adr(x)
        return CPU386.cast_adr_to_int(adr)

    all_null_registers = lltype.malloc(rffi.LONGP.TO, 24,
                                       flavor='raw', zero=True,
                                       immortal=True)

    def force(self, addr_of_force_index):
        TP = rffi.CArrayPtr(lltype.Signed)
        fail_index = rffi.cast(TP, addr_of_force_index)[0]
        assert fail_index >= 0, "already forced!"
        faildescr = self.get_fail_descr_from_number(fail_index)
        rffi.cast(TP, addr_of_force_index)[0] = ~fail_index
        frb = self.assembler._find_failure_recovery_bytecode(faildescr)
        bytecode = rffi.cast(rffi.UCHARP, frb)
        # start of "no gc operation!" block
        fail_index_2 = self.assembler.grab_frame_values(
            bytecode,
            addr_of_force_index - FORCE_INDEX_OFS,
            self.all_null_registers)
        self.assembler.leave_jitted_hook()
        # end of "no gc operation!" block
        assert fail_index == fail_index_2
        return faildescr

    def redirect_call_assembler(self, oldlooptoken, newlooptoken):
        self.assembler.redirect_call_assembler(oldlooptoken, newlooptoken)

    def invalidate_loop(self, looptoken):
        from pypy.jit.backend.x86 import codebuf
        
        for addr, tgt in looptoken.compiled_loop_token.invalidate_positions:
            mc = codebuf.MachineCodeBlockWrapper()
            mc.JMP_l(tgt)
            assert mc.get_relative_pos() == 5      # [JMP] [tgt 4 bytes]
            mc.copy_to_raw_memory(addr - 1)
        # positions invalidated
        looptoken.compiled_loop_token.invalidate_positions = []