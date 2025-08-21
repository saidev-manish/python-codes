import phonenumbers
from phonenumbers import geocoder, carrier, timezone, NumberParseException, PhoneNumberFormat, number_type, PhoneNumberType # type: ignore

def lookup():
    raw = input("Enter phone number with country code (e.g., +91 9876543210): ").strip()

    try:
        # Always parse as international; requires +<country_code>
        phone = phonenumbers.parse(raw, None)

        # Basic validation
        if not phonenumbers.is_possible_number(phone):
            print("❌ That number is not even possible for its country (length/pattern).")
            return
        if not phonenumbers.is_valid_number(phone):
            print("⚠️ The number format is valid, but it doesn't appear to be assigned/valid.")
            # continue anyway to show best-effort info

        # Formats
        e164 = phonenumbers.format_number(phone, PhoneNumberFormat.E164)
        intl = phonenumbers.format_number(phone, PhoneNumberFormat.INTERNATIONAL)
        natl = phonenumbers.format_number(phone, PhoneNumberFormat.NATIONAL)

        # Region / location (offline, usually reliable at country level)
        region = geocoder.description_for_number(phone, "en") or "Unknown"

        # Number type (mobile, fixed line, etc.)
        ntype = number_type(phone)
        ntype_str = {
            PhoneNumberType.MOBILE: "Mobile",
            PhoneNumberType.FIXED_LINE: "Fixed line",
            PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed line or Mobile",
            PhoneNumberType.TOLL_FREE: "Toll free",
            PhoneNumberType.PREMIUM_RATE: "Premium rate",
            PhoneNumberType.SHARED_COST: "Shared cost",
            PhoneNumberType.VOIP: "VoIP",
            PhoneNumberType.PERSONAL_NUMBER: "Personal number",
            PhoneNumberType.PAGER: "Pager",
            PhoneNumberType.UAN: "UAN",
            PhoneNumberType.VOICEMAIL: "Voicemail",
            PhoneNumberType.UNKNOWN: "Unknown"
        }.get(ntype, "Unknown")

        # Time zones (approximate)
        tzs = ", ".join(timezone.time_zones_for_number(phone)) or "Unknown"

        # Carrier (prefix-based; can be wrong if ported)
        provider = carrier.name_for_number(phone, "en") or "Unknown"

        print("\n=== Lookup Result (offline, best-effort) ===")
        print(f"Entered:         {raw}")
        print(f"E.164:           {e164}")
        print(f"International:   {intl}")
        print(f"National:        {natl}")
        print(f"Region:          {region}")
        print(f"Number type:     {ntype_str}")
        print(f"Time zone(s):    {tzs}")
        print(f"Carrier (static): {provider}")
        print("\nNote: Carrier is based on original number allocation and may be incorrect due to number portability.\n"
              "For live/accurate carrier & line status, use a real-time lookup API (e.g., Twilio Lookup / Numverify / Abstract).")

    except NumberParseException as e:
        print(f"❌ Could not parse the number: {e}\n"
              "Tip: include the + and country code, e.g. +91 9876543210")

if __name__ == "__main__":
    lookup()
