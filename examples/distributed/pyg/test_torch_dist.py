import os
import torch
import argparse
import intel_extension_for_pytorch as ipex
import oneccl_bindings_for_pytorch  # noqa
import torch.distributed as dist

num_nodes = 1

master_addr = "127.0.0.1" #'10.211.176.217'
master_port = "29500"# '11111'
os.environ["MASTER_ADDR"] = master_addr
os.environ["MASTER_PORT"] = master_port

node_rank = int(os.environ.get("RANK", -1))
mpi_rank = int(os.environ.get("PMI_RANK", -1))
mpi_world_size = int(os.environ.get("PMI_SIZE", -1))
rank = node_rank * mpi_world_size + mpi_rank
world_size = mpi_world_size * num_nodes
os.environ["RANK"] = str(rank)
os.environ["WORLD_SIZE"] = str(world_size)

print(
    f"node_rank: {node_rank}, mpi_rank: {mpi_rank} -> rank={rank}"
)
print(f"num_nodes: {num_nodes}, mpi_world_size:{mpi_world_size} -> world_size={world_size}")

dist.init_process_group(
    backend="ccl",
    rank=rank,
    world_size=world_size,
    init_method='tcp://{}:{}'.format(master_addr, master_port),
)
device = torch.device(f'xpu:{rank}')
print(f"{device}: ddp connected")
# dist.barrier()

# test_tensor = torch.tensor(rank)

# x = dist.all_reduce(test_tensor, op=dist.ReduceOp.SUM)
# print(x)
# print(f"Test value: {test_tensor.item()}, expected: {sum(range(world_size))}")
# dist.barrier()
# dist.destroy_process_group()