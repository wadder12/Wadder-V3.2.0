import io
import logging
import nextcord
from nextcord.ext import commands
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram

logging.basicConfig(level=logging.INFO)

# (ex:!qubit 0 1 0 ) then the bot should output something like (ex: Measurement result: {'010' : 1024})
        # for people who do not understand quant computing: the output is based on the inputs: the output means the prob of each state occuring after the measuremnt, 
        # which here is shown, meaning the 010 state occured 1024 time in the simulation. (means perf quant, no noise)

class QuantumComputing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def qubit(self, ctx, *operations: str):
        try:
            if not operations or len(operations) > 50:
                await ctx.send('Please provide a valid list of operations (up to 50).')
                return

            num_qubits = max([int(idx) for op in operations for idx in op.split(',')[1:]]) + 1
            if num_qubits > 10:
                await ctx.send('Please use up to 10 qubits only.')
                return

            qc = QuantumCircuit(num_qubits)

            for op in operations:
                op_parts = op.split(',')
                gate, qubits = op_parts[0], list(map(int, op_parts[1:]))

                if gate.upper() == 'X':
                    qc.x(*qubits)
                elif gate.upper() == 'H':
                    qc.h(*qubits)
                elif gate.upper() == 'CX':
                    qc.cx(*qubits)
                else:
                    await ctx.send(f"Invalid gate: {gate}. Supported gates: X, H, CX.")
                    return

            qc.measure_all()

            backend = Aer.get_backend('qasm_simulator')
            tqc = transpile(qc, backend)
            qobj = assemble(tqc, backend)
            result = backend.run(qobj, shots=1024).result()
            counts = result.get_counts(qc)

            # Generate histogram
            histogram = plot_histogram(counts)
            histogram_image = io.BytesIO()
            histogram.savefig(histogram_image, format='png')
            histogram_image.seek(0)

            # Send histogram image as a file attachment
            await ctx.send("Measurement result:", file=nextcord.File(histogram_image, 'result_histogram.png'))
        except Exception as e:
            logging.exception("Error in qubit command")
            await ctx.send(f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(QuantumComputing(bot))