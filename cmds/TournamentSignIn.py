import interactions as irt
import json
import os
import re

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class TournamentSignIn(irt.Extension):
    def __init__(self,client: irt.Client):
        self.client = client
        self.registration_cache = {}

    def _get_str(self, obj):
        if hasattr(obj, 'mention'): 
            return obj.mention    
        return str(obj)

    async def save_registration(self, uid, ctx):
        cache = self.registration_cache[uid]
        team_name = cache["team_name"]
        tournament_name = cache["tournament_name"]


        final_data = {
            "tournament_name": cache["tournament_name"],
            "team_name": cache["team_name"],
            "team_abbreviation": cache["team_abbreviation"],
            "contact_person_discord_id": cache["contact_person_discord_id"],
            "players": cache["players"],
            "other_members": cache["other_members"]
        }


        safe_name = re.sub(r'[^A-Za-z0-9_\-]', '_', team_name).strip('_') or 'team'
        os.makedirs('registrations', exist_ok=True)
        team_file = os.path.join('registrations', f'{safe_name}.json')
        
        existing_data = []
        if os.path.exists(team_file):
            with open(team_file, 'r', encoding='utf8') as f:
                try:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list): existing_data = []
                except: existing_data = []

        if any(team.get("tournament_name") == tournament_name for team in existing_data):
            await ctx.send(f"❌ Team **{team_name}** has already registered for **{tournament_name}**!")
            del self.registration_cache[uid]
            return

        existing_data.append(final_data)
        
        with open(team_file, 'w', encoding='utf8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)


        del self.registration_cache[uid]

        await ctx.send(f"🎉 **Registration Complete!**\nTeam: {team_name}\nTournament: {tournament_name}")
    
    async def name_to_id(self, ctx, user_input: str):
        if not user_input: return None
        target_name = user_input.strip().lstrip("@").lower()

        if re.match(r"^<@!?\d+>$", target_name) or target_name.isdigit():
             return f"<@{target_name.strip('<@!>')}>"

        for member in ctx.guild.members:
            if member.user.username == target_name:
                return f"<@{member.id}>"
        return None
    
    @irt.slash_command( #add tournament
        name="add_tournament",
        description="Add a VBL tournament.",
        default_member_permissions=irt.Permissions.ADMINISTRATOR #admin only
    )
    @irt.slash_option( 
        name="tournament_name",
        description="The tournament you want to add.",
        opt_type=irt.OptionType.STRING,
        required=True,
    )
    async def add_tournament(self, ctx, tournament_name):
        if tournament_name not in jdata["tournament_list"]:
            jdata["tournament_list"].append(tournament_name)
            with open('setting.json','w',encoding='utf8') as jfile:
                json.dump(jdata, jfile, ensure_ascii=False, indent=2)  
        await ctx.send(f"Tournament '{tournament_name}' has been added.")
        

    @irt.slash_command( #remove tournament
        name="remove_tournament",
        description="Remove a VBL tournament. ",
        default_member_permissions=irt.Permissions.ADMINISTRATOR #admin only
    )
    @irt.slash_option(
        name="tournament_name",
        description="The tournament you want to remove.",
        opt_type=irt.OptionType.STRING,
        required=True,
        choices=[
            {"name": tournament, "value": tournament} 
            for tournament in jdata["tournament_list"]
        ]
    )
    async def remove_tournament(self, ctx, tournament_name):
        if tournament_name in jdata["tournament_list"]:
            jdata["tournament_list"].remove(tournament_name)
            with open('setting.json','w',encoding='utf8') as jfile:
                json.dump(jdata, jfile, ensure_ascii=False, indent=2) 
        await ctx.send(f"Tournament '{tournament_name}' has been removed.")


    @irt.slash_command(
        name="register",
        description="Register for the VBL tournament. ",
    )
    @irt.slash_option(
        name="tournament_name",
        description="The tournament you want to register.",
        opt_type=irt.OptionType.STRING,
        required=True,
        choices=[
            {"name": t, "value": t} 
            for t in jdata["tournament_list"]
        ]
    )
    @irt.slash_option(name="team_name", description="Your team's name.", opt_type=irt.OptionType.STRING, required=True, min_length=3, max_length=15)
    @irt.slash_option(name="team_abbreviation", description="Team abbreviation.", opt_type=irt.OptionType.STRING, required=True, min_length=2, max_length=4)
    @irt.slash_option(name="contact_person_discord_id", description="Contact Person Discord ID", opt_type=irt.OptionType.MENTIONABLE, required=True)
    @irt.slash_option(name="player1_discord_id", description="P1 Discord ID", opt_type=irt.OptionType.MENTIONABLE, required=True)
    @irt.slash_option(name="player1_valorant_id", description="P1 Valorant ID", opt_type=irt.OptionType.STRING, required=True)
    @irt.slash_option(name="player2_discord_id", description="P2 Discord ID", opt_type=irt.OptionType.MENTIONABLE, required=True)
    @irt.slash_option(name="player2_valorant_id", description="P2 Valorant ID", opt_type=irt.OptionType.STRING, required=True)
    @irt.slash_option(name="player3_discord_id", description="P3 Discord ID", opt_type=irt.OptionType.MENTIONABLE, required=True)
    @irt.slash_option(name="player3_valorant_id", description="P3 Valorant ID", opt_type=irt.OptionType.STRING, required=True)
    @irt.slash_option(name="player4_discord_id", description="P4 Discord ID", opt_type=irt.OptionType.MENTIONABLE, required=True)
    @irt.slash_option(name="player4_valorant_id", description="P4 Valorant ID", opt_type=irt.OptionType.STRING, required=True)
    @irt.slash_option(name="player5_discord_id", description="P5 Discord ID", opt_type=irt.OptionType.MENTIONABLE, required=True)
    @irt.slash_option(name="player5_valorant_id", description="P5 Valorant ID", opt_type=irt.OptionType.STRING, required=True)
    @irt.slash_option(name="other_member1_discord_id", description="OM1 Discord ID", opt_type=irt.OptionType.MENTIONABLE, required=False)
    @irt.slash_option(name="other_member1_valorant_id", description="OM1 Valorant ID", opt_type=irt.OptionType.STRING, required=False)
    @irt.slash_option(name="other_member2_discord_id", description="OM2 Discord ID", opt_type=irt.OptionType.MENTIONABLE, required=False)
    @irt.slash_option(name="other_member2_valorant_id", description="OM2 Valorant ID", opt_type=irt.OptionType.STRING, required=False)
    async def register(self, ctx,
                       tournament_name, team_name, team_abbreviation, contact_person_discord_id,
                       player1_discord_id, player1_valorant_id,
                       player2_discord_id, player2_valorant_id,
                       player3_discord_id, player3_valorant_id,
                       player4_discord_id, player4_valorant_id,
                       player5_discord_id, player5_valorant_id,
                       other_member1_discord_id=None, other_member1_valorant_id=None,
                       other_member2_discord_id=None, other_member2_valorant_id=None):

        registration_data = {
            "tournament_name": tournament_name,
            "team_name": team_name,
            "team_abbreviation": team_abbreviation,
            "contact_person_discord_id": self._get_str(contact_person_discord_id),
            "players": [
                {"discord_id": self._get_str(player1_discord_id), "valorant_id": player1_valorant_id},
                {"discord_id": self._get_str(player2_discord_id), "valorant_id": player2_valorant_id},
                {"discord_id": self._get_str(player3_discord_id), "valorant_id": player3_valorant_id},
                {"discord_id": self._get_str(player4_discord_id), "valorant_id": player4_valorant_id},
                {"discord_id": self._get_str(player5_discord_id), "valorant_id": player5_valorant_id}
            ],
            "other_members": []
        }

        if other_member1_discord_id and other_member1_valorant_id:
            registration_data["other_members"].append(
                {"discord_id": self._get_str(other_member1_discord_id), "valorant_id": other_member1_valorant_id}
            )
        if other_member2_discord_id and other_member2_valorant_id:
            registration_data["other_members"].append(
                {"discord_id": self._get_str(other_member2_discord_id), "valorant_id": other_member2_valorant_id}
            )

        safe_name = re.sub(r'[^A-Za-z0-9_\-]', '_', team_name).strip('_') or 'team'
        os.makedirs('registrations', exist_ok=True)
        team_file = os.path.join('registrations', f'{safe_name}.json')
        data = []

        if os.path.exists(team_file):
            with open(team_file, 'r', encoding='utf8') as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []

        if any(team["tournament_name"] == tournament_name for team in data):
            await ctx.send(f"{team_name} has already registered {tournament_name}！")
            return
        
        data.append(registration_data)
        with open(team_file, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        await ctx.send(f"Register saved! Team:{team_name} Tournament:({tournament_name})")

    @irt.slash_command(
        name = "register_modal",
        description = "register_modal command",
        default_member_permissions=irt.Permissions.ADMINISTRATOR #admin only
    )
    async def register_modal(self, ctx):
        select_options = [
            irt.StringSelectOption(label=tournament_name, value=tournament_name)
            for tournament_name in jdata["tournament_list"]
        ]

        tournament_select = irt.StringSelectMenu(
            *select_options,
            placeholder="Choose the tournament you want to register",
            custom_id="tournament_select",
            min_values=1,
            max_values=1
        )
        await ctx.send("**Choose the tournament you want to register:**", components=tournament_select)
        
    @irt.component_callback("tournament_select")
    async def callback_tournament_select(self, ctx):
        selected_tournament = ctx.values[0]

        self.registration_cache[str(ctx.author.id)] = {
            "tournament_name": selected_tournament,
            "players": [],
            "other_members": []
        }
        await self.open_step1_modal(ctx)

    async def open_step1_modal(self, ctx, defaults=None):
        if defaults is None: defaults = {}
        
        modal1 = irt.Modal(
            irt.InputText(label="Team Name", custom_id="team_name", style=irt.TextStyles.SHORT, required=True, placeholder="Team Name (3-15 chars)", value=defaults.get("team_name", "")),
            irt.InputText(label="Abbreviation", custom_id="team_abbr", style=irt.TextStyles.SHORT, required=True, placeholder="3-4 chars (A-Z, 0-9)", value=defaults.get("team_abbr", "")),
            irt.InputText(label="Contact Person Discord ID", custom_id="cp_discord", style=irt.TextStyles.SHORT, required=True, placeholder="@username", value=defaults.get("cp_discord", "")),
            title=defaults.get("title", "Step 1: Team Info"),
            custom_id="modal_step1",
        )
        await ctx.send_modal(modal1)

    @irt.component_callback("retry_step1")
    async def retry_step1(self, ctx):
        uid = str(ctx.author.id)
        if uid not in self.registration_cache:
            await ctx.send("Session expired.", ephemeral=True)
            return

        cache_data = self.registration_cache[uid]
        defaults = {
            "team_name": cache_data.get("team_name", ""),
            "team_abbr": cache_data.get("team_abbreviation", ""),
            "cp_discord": cache_data.get("raw_cp", ""), 
            "title": "⚠️ Retry: Fix Errors"
        }
        await self.open_step1_modal(ctx, defaults)

    @irt.modal_callback("modal_step1")
    async def modal_step1(self, ctx, team_name: str, team_abbr: str, cp_discord: str):
        uid = str(ctx.author.id)
        if uid not in self.registration_cache:
            await ctx.send("Session expired. Please start over.", ephemeral=True)
            return
        
       
        name_len = len(team_name)
        abbr_len = len(team_abbr)
        is_abbr_alnum = team_abbr.isalnum()
        formatted_mention = await self.name_to_id(ctx, cp_discord)
        
        err_name = not (3 <= name_len <= 15)
        err_abbr = not (2 <= abbr_len <= 4 and is_abbr_alnum)
        err_user = formatted_mention is None

        if err_name or err_abbr or err_user:
            self.registration_cache[uid]["team_name"] = team_name
            self.registration_cache[uid]["team_abbreviation"] = team_abbr
            self.registration_cache[uid]["raw_cp"] = cp_discord # 暫存原始輸入

            error_msg = "❌ **Errors Found:**\n"
            if err_name: error_msg += "- Team Name must be 3-15 chars.\n"
            if err_abbr: error_msg += "- Abbreviation must be 2-4 alphanumeric chars.\n"
            if err_user: error_msg += "- Contact Person not found (check username).\n"
            
            btn = irt.Button(label="🔄 Click to Fix", custom_id="retry_step1", style=irt.ButtonStyle.DANGER)
            await ctx.send(error_msg, components=btn, ephemeral=True)
            return

        self.registration_cache[uid]["team_name"] = team_name
        self.registration_cache[uid]["team_abbreviation"] = team_abbr
        self.registration_cache[uid]["contact_person_discord_id"] = formatted_mention

        btn = irt.Button(label="Next: Add Players 1 & 2", custom_id="btn_goto_step2", style=irt.ButtonStyle.PRIMARY)
        await ctx.send(f"✅ Team **{team_name}** info saved.\nClick below to add players.", components=btn, ephemeral=True)

    @irt.component_callback("btn_goto_step2")
    async def btn_step2(self, ctx):
        uid = str(ctx.author.id)

        players = self.registration_cache.get(uid, {}).get("raw_players_step2", {})
        
        modal2 = irt.Modal(
            irt.InputText(label="Player1 Discord ID", custom_id="p1_discord", style=irt.TextStyles.SHORT, required=True, placeholder="@username", value=players.get("p1_d", "")),
            irt.InputText(label="Player1 Valorant ID", custom_id="p1_val", style=irt.TextStyles.SHORT, required=True, placeholder="Name#Tag", value=players.get("p1_v", "")),
            irt.InputText(label="Player2 Discord ID", custom_id="p2_discord", style=irt.TextStyles.SHORT, required=True, placeholder="@username", value=players.get("p2_d", "")),
            irt.InputText(label="Player2 Valorant ID", custom_id="p2_val", style=irt.TextStyles.SHORT, required=True, placeholder="Name#Tag", value=players.get("p2_v", "")),
            title="Step 2: Players 1 & 2",
            custom_id="modal_step2"
        )
        await ctx.send_modal(modal2)

    @irt.modal_callback("modal_step2")
    async def modal_step2(self, ctx, p1_discord: str, p1_val: str, p2_discord: str, p2_val: str):
        uid = str(ctx.author.id)
        if uid not in self.registration_cache:
            await ctx.send("Session expired.", ephemeral=True)
            return
        
        p1_id = await self.name_to_id(ctx, p1_discord)
        p2_id = await self.name_to_id(ctx, p2_discord)

        if p1_id is None or p2_id is None:

            self.registration_cache[uid]["raw_players_step2"] = {
                "p1_d": p1_discord, "p1_v": p1_val,
                "p2_d": p2_discord, "p2_v": p2_val
            }
            error_msg = "❌ **User Not Found:**\n"
            if p1_id is None: error_msg += "- Player 1 not found.\n"
            if p2_id is None: error_msg += "- Player 2 not found.\n"


            btn = irt.Button(label="🔄 Click to Fix", custom_id="btn_goto_step2", style=irt.ButtonStyle.DANGER)
            await ctx.send(error_msg, components=btn, ephemeral=True)
            return

        self.registration_cache[uid]["players"].append({"discord_id": p1_id, "valorant_id": p1_val})
        self.registration_cache[uid]["players"].append({"discord_id": p2_id, "valorant_id": p2_val})

        btn = irt.Button(label="Next: Add Players 3&4", custom_id="btn_goto_step3", style=irt.ButtonStyle.PRIMARY)
        await ctx.send("✅ P1 & P2 saved. Next step...", components=btn, ephemeral=True)
    
    @irt.component_callback("btn_goto_step3")
    async def btn_step3(self, ctx):
        uid = str(ctx.author.id)
        players = self.registration_cache.get(uid, {}).get("raw_players_step3", {})

        modal3 = irt.Modal(
            irt.InputText(label="Player 3 Discord ID", custom_id="p3_discord", style=irt.TextStyles.SHORT, required=True, placeholder="@username", value=players.get("p3_d", "")),
            irt.InputText(label="Player 3 Valorant ID", custom_id="p3_val", style=irt.TextStyles.SHORT, required=True, value=players.get("p3_v", "")),
            irt.InputText(label="Player 4 Discord ID", custom_id="p4_discord", style=irt.TextStyles.SHORT, required=True, placeholder="@username", value=players.get("p4_d", "")),
            irt.InputText(label="Player 4 Valorant ID", custom_id="p4_val", style=irt.TextStyles.SHORT, required=True, value=players.get("p4_v", "")),
            title="Step 3: Players 3, 4, 5",
            custom_id="modal_step3"
        )
        await ctx.send_modal(modal3)
    
    @irt.modal_callback("modal_step3")
    async def modal_step3_submit(self, ctx, p3_discord, p3_val, p4_discord, p4_val):
        uid = str(ctx.author.id)
        if uid not in self.registration_cache:
            await ctx.send("Session expired.", ephemeral=True)
            return

        p3_id = await self.name_to_id(ctx, p3_discord)
        p4_id = await self.name_to_id(ctx, p4_discord)

        if p3_id is None or p4_id is None:
            self.registration_cache[uid]["raw_players_step3"] = {
                "p3_d": p3_discord, "p3_v": p3_val,
                "p4_d": p4_discord, "p4_v": p4_val
            }
            error_msg = "❌ **User Not Found:**\n"
            if p3_id is None: error_msg += "- Player 3 not found.\n"
            if p4_id is None: error_msg += "- Player 4 not found.\n"

            btn = irt.Button(label="🔄 Click to Fix", custom_id="btn_goto_step3", style=irt.ButtonStyle.DANGER)
            await ctx.send(error_msg, components=btn, ephemeral=True)
            return

        self.registration_cache[uid]["players"].append({"discord_id": p3_id, "valorant_id": p3_val})
        self.registration_cache[uid]["players"].append({"discord_id": p4_id, "valorant_id": p4_val})

        btn = irt.Button(label="Next: Player 5 & Other members", custom_id="btn_goto_step4", style=irt.ButtonStyle.BLUE)
        await ctx.send("✅ P3 & P4 saved. Next step...", components=btn, ephemeral=True)

    @irt.component_callback("btn_goto_step4")
    async def btn_step4(self, ctx):
        uid = str(ctx.author.id)
        data = self.registration_cache.get(uid, {}).get("raw_step4", {})

        modal4 = irt.Modal(
            irt.InputText(label="Player 5 Discord ID", custom_id="p5_discord", style=irt.TextStyles.SHORT, required=True, placeholder="@username", value=data.get("p5_d", "")),
            irt.InputText(label="Player 5 Valorant ID", custom_id="p5_val", style=irt.TextStyles.SHORT, required=True, value=data.get("p5_v", "")),
            irt.InputText(label="Othermember1 Discord ID", custom_id="om1_discord", style=irt.TextStyles.SHORT, required=False, placeholder="@username", value=data.get("om1_d", "")),
            irt.InputText(label="Othermember1 Valorant ID", custom_id="om1_val", style=irt.TextStyles.SHORT, required=False, placeholder="Name#Tag", value=data.get("om1_v", "")),
            irt.InputText(label="addmore?", custom_id="addmore", style=irt.TextStyles.SHORT, required=True, placeholder=" 1=Yes | 0=No ", value=data.get("add", "")),
            title="Step 4: Player 5 & Other Members",
            custom_id="modal_step4"
        )
        await ctx.send_modal(modal4)
    
    @irt.modal_callback("modal_step4")
    async def modal_step4(self, ctx, p5_discord: str, p5_val: str, om1_discord: str, om1_val: str, addmore: str):
        uid = str(ctx.author.id)
        if uid not in self.registration_cache:
            await ctx.send("Session expired.", ephemeral=True)
            return

        p5_id = await self.name_to_id(ctx, p5_discord)
        
        om1_id = None
        om1_error = False
        if om1_discord:
            om1_id = await self.name_to_id(ctx, om1_discord)
            if om1_id is None: om1_error = True

        clean_addmore = addmore.strip()
        addmore_error = clean_addmore not in ["0", "1"]

        if p5_id is None or om1_error or addmore_error:
            self.registration_cache[uid]["raw_step4"] = {
                "p5_d": p5_discord, "p5_v": p5_val,
                "om1_d": om1_discord, "om1_v": om1_val,
                "add": addmore
            }
            error_msg = "❌ **Errors Found:**\n"
            if p5_id is None: error_msg += "- Player 5 not found.\n"
            if om1_error: error_msg += "- Other Member 1 not found.\n"
            if addmore_error: error_msg += "- 'addmore' must be 0 or 1.\n"

            btn = irt.Button(label="🔄 Click to Fix", custom_id="btn_goto_step4", style=irt.ButtonStyle.DANGER)
            await ctx.send(error_msg, components=btn, ephemeral=True)
            return

        self.registration_cache[uid]["players"].append({"discord_id": p5_id, "valorant_id": p5_val})

        if om1_id and om1_val:
            self.registration_cache[uid]["other_members"].append({"discord_id": om1_id, "valorant_id": om1_val})

        if clean_addmore == "1":

            btn = irt.Button(label="Next: Add Other Member 2", custom_id="btn_goto_step5", style=irt.ButtonStyle.PRIMARY)
            await ctx.send("✅ Step 4 saved. Click below to continue.", components=btn, ephemeral=True)
        else:
            await self.save_registration(uid, ctx)


    @irt.component_callback("btn_goto_step5")
    async def btn_step5(self, ctx):
        await self.open_step5_modal(ctx)

    async def open_step5_modal(self, ctx, defaults=None):
        if defaults is None: defaults = {}
        modal5 = irt.Modal(
            irt.InputText(label="Othermember2 Discord ID", custom_id="om2_discord", style=irt.TextStyles.SHORT, required=False, placeholder="@username", value=defaults.get("om2_d", "")),
            irt.InputText(label="Othermember2 Valorant ID", custom_id="om2_val", style=irt.TextStyles.SHORT, required=False, placeholder="Name#Tag", value=defaults.get("om2_v", "")),
            title="Step 5 : Other Member 2",
            custom_id="modal_step5"
        )
        await ctx.send_modal(modal5)


    @irt.component_callback("retry_step5")
    async def retry_step5(self, ctx):
        uid = str(ctx.author.id)
        raw_data = self.registration_cache.get(uid, {}).get("raw_step5", {})
        await self.open_step5_modal(ctx, raw_data)

    @irt.modal_callback("modal_step5")
    async def modal_step5(self, ctx, om2_discord: str, om2_val: str):
        uid = str(ctx.author.id)
        if uid not in self.registration_cache:
            await ctx.send("Session expired.", ephemeral=True)
            return
        
        om2_id = None
        if om2_discord and om2_val:
            om2_id = await self.name_to_id(ctx, om2_discord)
            
            if om2_id is None:
                self.registration_cache[uid]["raw_step5"] = {"om2_d": om2_discord, "om2_v": om2_val}
                btn = irt.Button(label="🔄 Click to Fix", custom_id="retry_step5", style=irt.ButtonStyle.DANGER)
                await ctx.send("❌ **User Not Found:** Other Member 2 not found.", components=btn, ephemeral=True)
                return

            self.registration_cache[uid]["other_members"].append({"discord_id": om2_id, "valorant_id": om2_val})
        
        await self.save_registration(uid, ctx)