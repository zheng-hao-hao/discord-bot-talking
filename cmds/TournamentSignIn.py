import interactions
import json
import os
import re

class TournamentSignIn(interactions.Extension):
   def __init__(self,client: interactions.Client):
      self.client = client

   @interactions.slash_command(
    name="register",
    description="Register for the VBL tournament. ",
    options=
      [
      interactions.SlashCommandOption # Tournament Name
      (
          name="tournament_name",
          description="The tournament you want to register.",
          type=interactions.OptionType.STRING,
          required=True,
      ),
       interactions.SlashCommandOption #Team Name
      (
          name="team_name",
          description="Your team's name.",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Team abbreviation 
      (
          name="team_abbreviation",
          description="Your team's abbreviation (alphabets and numbers only, 3-4 letters.).",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Contact person's Discord ID
      (
          name="contact_person_discord_id",
          description="Your team's contact person's Discord ID(e.g. @abc123).",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Player 1 Discord ID
      (
          name="player1_discord_id",
          description="Player 1 Discord ID (e.g. @abc123).",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Player 1 VALORANT ID
      (
          name="player1_valorant_id",
          description="Player 1 VALORANT ID (e.g. abc#123).",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Player 2 Discord ID
      (
          name="player2_discord_id",
          description="Player 2 Discord ID (e.g. @abc123).",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Player 2 VALORANT ID
      (
          name="player2_valorant_id",
          description="Player 2 VALORANT ID (e.g. abc#123).",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Player 3 Discord ID
      (
          name="player3_discord_id",
          description="Player 3 Discord ID (e.g. @abc123).",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Player 3 VALORANT ID
      (
          name="player3_valorant_id",
          description="Player 3 VALORANT ID (e.g. abc#123).",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Player 4 Discord ID
      (
          name="player4_discord_id",
          description="Player 4 Discord ID (e.g. @abc123).",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Player 4 VALORANT ID
      (
          name="player4_valorant_id",
          description="Player 4 VALORANT ID (e.g. abc#123).",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Player 5 Discord ID
      (
          name="player5_discord_id",
          description="Player 5 Discord ID (e.g. @abc123).",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Player 5 VALORANT ID
      (
          name="player5_valorant_id",
          description="Player 5 VALORANT ID (e.g. abc#123).",
          type=interactions.OptionType.STRING,
          required=True,
      ),
      interactions.SlashCommandOption #Other member 1 Discord ID
      (
          name="other_member1_discord_id",
          description="Other member 1 Discord ID (e.g. @abc123).",
          type=interactions.OptionType.STRING,
          required=False,
      ),
      interactions.SlashCommandOption #Other member 1 VALORANT ID
      (
          name="other_member1_valorant_id",
          description="Other member 1 VALORANT ID (e.g. abc#123).",
          type=interactions.OptionType.STRING,
          required=False,
      ),
      interactions.SlashCommandOption #Other member 2 Discord ID
      (
          name="other_member2_discord_id",
          description="Other member 2 Discord ID (e.g. @abc123).",
          type=interactions.OptionType.STRING,
          required=False,
      ),
      interactions.SlashCommandOption #Other member 2 VALORANT ID
      (
          name="other_member2_valorant_id",
          description="Other member 2 VALORANT ID (e.g. abc#123).",
          type=interactions.OptionType.STRING,
          required=False,
      )
      ]
   )
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
             "contact_person_discord_id": contact_person_discord_id,
             "players": [
                 {"discord_id": player1_discord_id, "valorant_id": player1_valorant_id},
                 {"discord_id": player2_discord_id, "valorant_id": player2_valorant_id},
                 {"discord_id": player3_discord_id, "valorant_id": player3_valorant_id},
                 {"discord_id": player4_discord_id, "valorant_id": player4_valorant_id},
                 {"discord_id": player5_discord_id, "valorant_id": player5_valorant_id}
             ],
             "other_members": []
         }
    
         if other_member1_discord_id and other_member1_valorant_id:
              registration_data["other_members"].append(
                {"discord_id": other_member1_discord_id, "valorant_id": other_member1_valorant_id}
              )
         if other_member2_discord_id and other_member2_valorant_id:
              registration_data["other_members"].append(
                {"discord_id": other_member2_discord_id, "valorant_id": other_member2_valorant_id}
              )
    
         safe_name = re.sub(r'[^A-Za-z0-9_\-]', '_', team_name).strip('_') or 'team'
         os.makedirs('registrations', exist_ok=True)
         team_file = os.path.join('registrations', f'{safe_name}.json')

         try:
             with open(team_file, 'r', encoding='utf8') as f:
                 data = json.load(f)
                 if not isinstance(data, list):
                     data = []
         except FileNotFoundError:
             data = []

         data.append(registration_data)
         with open(team_file, 'w', encoding='utf8') as f:
             json.dump(data, f, ensure_ascii=False, indent=2)

         await ctx.send(f"報名已儲存：{team_file}")