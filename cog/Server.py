import discord
from discord.ext import commands
from discord.ext.commands import command
import digitalocean
from digitalocean.baseapi import BaseAPI
import os

token = os.environ["DigitalOcean_token"]
domain_name = os.environ["Domain_name"]


manager = digitalocean.Manager(token=token)
image_id = manager.get_my_images()[0].id
keys = manager.get_all_sshkeys()


def get_my_image():
    for my_image in manager.get_my_images():
        if my_image.name in "world":
            return my_image
        if len(manager.get_my_images()) == 1:
            return my_image


droplet = digitalocean.Droplet(token=token,
                               name="minecraft-server",
                               region="sgp1",
                               size_slug="",
                               image=str(get_my_image().id),
                               ssh_keys=keys)

print(get_my_image().id)
domain = digitalocean.Domain(token=token, name=domain_name)

params = {}


class Server(commands.Cog, BaseAPI):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.embed = discord.Embed()
        self.record_id = None
        self.my_image = None

    @command()
    async def start(self, ctx):
        await ctx.send("```起動中```")
        droplet.create()

        action = droplet.get_events()[0]
        action.wait()
        ip = droplet.load().ip_address
        domain.create_new_domain_record(
            type="A", name="@", data=str(ip), ttl=30)
        await ctx.send("```起動完了```")

        if get_my_image().name in "world":
            get_my_image().destroy()

    @command()
    async def sstop(self, ctx):
        _droplet = manager.get_all_droplets()[0]
        _droplet.take_snapshot(snapshot_name="world")
        action = droplet.get_events()[0]
        action.wait()

        data = domain.get_records()

        for record_data in data:
            if record_data.type in "A":
                self.record_id = record_data.id
                break

        record = digitalocean.Record(token=token, domain_name=domain_name)
        record.id = str(self.record_id)

        record.destroy()

        res = _droplet.destroy()
        print(res)


def setup(bot):
    return bot.add_cog(Server(bot))
